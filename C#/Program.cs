// ------------------------------------------------------------------------------
// <copyright file="Program.cs">
//   Main methods for pre-processing the Maluuba frames dataset
// </copyright>
// ------------------------------------------------------------------------------

namespace ParseFrames
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Text;
    using Newtonsoft.Json;
    using Newtonsoft.Json.Linq;

    class Program
    {
        static readonly Dictionary<string, List<StructedData>> frameMap = new Dictionary<string, List<StructedData>>();

        static void Main(string[] args)
        {
            string pathToFramesDataSet = @"C:\Users\v-riach\Downloads\Frames-dataset\frames.json";
            SpellCheck(pathToFramesDataSet);
            GenerateDataForNER(pathToFramesDataSet);
            GenerateDataforClassifiers(pathToFramesDataSet);

        }

        private static void GenerateDataForNER(string path)
        {
            var data = ExtractFirstConversation(path);
            StringBuilder b = new StringBuilder();
            foreach (var structedData in data)
            {
                var text = structedData.Text.Replace("\n", "");
                text = text.Replace(";", "");

                b.AppendLine(
                    $"{structedData.User};{structedData.Intent};{text};{structedData.Origin};" +
                    $"{structedData.Destination};{structedData.Adults};" +
                    $"{structedData.Budget}; {structedData.Date}; {structedData.FrameNumber}");
            }


            File.WriteAllText(@"c:\temp\conversations\structured1.txt", b.ToString());
        }


        private static void SpellCheck(string path)
        {
            var file = File.ReadAllText(path);
            var json = JsonConvert.DeserializeObject<List<RootObject>>(file);
            var index = 0;
            foreach (var rootObject in json)
            {
                List<string>newLines = new List<string>();
                foreach (var turns in rootObject.turns)
                {
                    try
                    {
                        var result = BingSpellCheck.SpellCheck(turns.text);
                        newLines.Add(result);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine(e);
                    }
                }
                File.WriteAllLines($"C:\\temp\\conversations\\spell\\{index}.txt", newLines);
                index++;
            }
           
        }

        private static void GenerateDataforClassifiers(string path)
        {
            var data = ExtractFirstConversation(path);
            StringBuilder b = new StringBuilder();
            b.AppendLine(
                $"PrevIntent;PrevOrigin;PrevAdults;PrevBudget;PrevDate;PrevDestination;ConversationId;User;Intent;text;Origin;Destination;" +
                $"Adults;Budget;Date;FrameNumber;FrameSwitched");

            foreach (var structedData in data)
            {
                var text = structedData.Text.Replace("\n", "");
                text = text.Replace(";", "");
                var switchval = 0;
                switchval = structedData.FrameSwitched ? 1 : 0;
                if (switchval == 1)
                {
                    for (int i = 0; i < 4; i++)
                    {
                        b.AppendLine(
                            $"{structedData.PrevIntent};{structedData.PrevOrigin};{structedData.PrevAdults};{structedData.PrevBudget};" +
                            $"{structedData.PrevDate};{structedData.PrevDestination};" +
                            $"{structedData.ConversationId}; {structedData.User}; {structedData.Intent}; {text}; {structedData.Origin}; {structedData.Destination}; " +
                            $"{structedData.Adults}; {structedData.Budget}; {structedData.Date}; {structedData.FrameNumber}; {switchval}");
                    }
                }
                else
                {
                    b.AppendLine(
                        $"{structedData.PrevIntent};{structedData.PrevOrigin};{structedData.PrevAdults};{structedData.PrevBudget};" +
                        $"{structedData.PrevDate};{structedData.PrevDestination};" +
                        $"{structedData.ConversationId}; {structedData.User}; {structedData.Intent}; {text}; {structedData.Origin}; {structedData.Destination}; " +
                        $"{structedData.Adults}; {structedData.Budget}; {structedData.Date}; {structedData.FrameNumber}; {switchval}");
                }
            }

            File.WriteAllText(@"c:\temp\conversations\structured_conv.txt", b.ToString());
        }


        private static List<StructedData> ExtractFirstConversation(string path)
        {
            var file = File.ReadAllText(path);
            var json = JsonConvert.DeserializeObject<List<RootObject>>(file);
            var index = 0;
            var dataList = new List<StructedData>();
            var none = "none";

            foreach (var rootObject in json)
            {
                StructedData current = null;
                index++;
                foreach (var turns in rootObject.turns)
                {
                    var data = new StructedData
                    {
                        Text = turns.text,
                        User = turns.author,
                        FrameNumber = turns.labels.active_frame.ToString(),
                        ConversationId = rootObject.id
                    };

                    if (current != null)
                    {
                        if (data.FrameNumber != current.FrameNumber)
                        {
                            data.FrameSwitched = true;
                        }

                        data.PrevAdults = string.IsNullOrEmpty(current.Adults) ? none : current.Adults;
                        data.PrevBudget = string.IsNullOrEmpty(current.Budget) ? none : current.Budget;
                        data.PrevDate = string.IsNullOrEmpty(current.Date) ? none : current.Date;
                        data.PrevDestination = string.IsNullOrEmpty(current.Destination) ? none : current.Destination;
                        data.PrevOrigin = string.IsNullOrEmpty(current.Origin) ? none : current.Origin;
                        data.PrevIntent = string.IsNullOrEmpty(current.Intent) ? none : current.Intent;
                    }
                    else
                    {
                        data.PrevAdults = none;
                        data.PrevBudget = none;
                        data.PrevDate = none;
                        data.PrevDestination = none;
                        data.PrevOrigin = none;
                        data.PrevIntent = none;
                    }

                    foreach (var turnsLabel in turns.labels.acts)
                    {
                        foreach (JToken turnsLabelArg in turnsLabel.args)
                        {
                            var children = turnsLabelArg.Children();
                            var first = (JProperty)children.First();
                            var value = first.Value.ToString();
                            var second = (JProperty)children.Last();
                            var key = second.Value.ToString();
                            UpdateData(key, value, data);
                        }
                    }

                    dataList.Add(data);
                    current = data;
                }
            }

            return dataList;
        }

        private static void UpdateData(string key, string value, StructedData data)
        {
            if (value == key)
            {
                return;
            }

            switch (key)
            {
                case "intent":
                    data.Intent = value;
                    break;
                case "dst_city":
                    data.Destination = value;
                    break;
                case "or_city":
                    data.Origin = value;
                    break;
                case "str_date":
                    data.Date = value;
                    break;
                case "n_adults":
                    data.Adults = value;
                    break;
                case "budget":
                    data.Budget = value;
                    break;
            }
        }
    }

    /// <summary>
    /// Object representation of the CSV file generated
    /// </summary>
    public class StructedData
    {
        public string Text { get; set; }
        public string User { get; set; }
        public string Intent { get; set; }
        public string Origin { get; set; }
        public string Destination { get; set; }
        public string Adults { get; set; }
        public string Budget { get; set; }
        public string Date { get; set; }

        public string PrevIntent { get; set; }

        public string PrevOrigin { get; set; }
        public string PrevDestination { get; set; }
        public string PrevAdults { get; set; }
        public string PrevBudget { get; set; }
        public string PrevDate { get; set; }
        public bool FrameSwitched { get; set; }
        public string FrameNumber { get; set; }

        public int PredictedFrameNumber { get; set; }

        public string ConversationId { get; set; }
    }
}
