// ------------------------------------------------------------------------------
// <copyright file="BingSpellCheck.cs">
//   Class used to call the Bing Spell Check API for the turns in the Maluuba frames data
// </copyright>
// ------------------------------------------------------------------------------

namespace ParseFrames
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Net.Http;
    using System.Net.Http.Headers;
    using System.Text;
    using Newtonsoft.Json;

    /// <summary>
    /// This file contains code from the sample program provided at
    /// https://docs.microsoft.com/en-us/azure/cognitive-services/speech/how-to/how-to-authentication?tabs=CSharp
    /// </summary>
    class BingSpellCheck
    {
        static readonly string host = "https://api.cognitive.microsoft.com";
        static readonly string path = "/bing/v7.0/spellcheck?";

        // For a list of available markets, go to:
        // https://docs.microsoft.com/rest/api/cognitiveservices/bing-autosuggest-api-v7-reference#market-codes
        static readonly string params_ = "mkt=en-US&mode=proof";

        // NOTE: Replace this example key with a valid subscription key.
        static readonly string key = "mykey";
        
       
        public static string SpellCheck(string text)
        {
            HttpClient client = new HttpClient();
            client.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", key);
          

            HttpResponseMessage response = new HttpResponseMessage();
            string uri = host + path + params_;

            List<KeyValuePair<string, string>> values = new List<KeyValuePair<string, string>>();
            values.Add(new KeyValuePair<string, string>("text", text));

            using (FormUrlEncodedContent content = new FormUrlEncodedContent(values))
            {
                content.Headers.ContentType = new MediaTypeHeaderValue("application/x-www-form-urlencoded");
                try
                {
                    response = client.PostAsync(uri, content).Result;
                }
                catch (Exception e)
                {
                    Console.WriteLine(e);
                }

            }
            

            string contentString = response.Content.ReadAsStringAsync().Result;
            var json = JsonConvert.DeserializeObject<global::RootObject>(contentString);
            if (json != null)
            {
                foreach (var flaggedToken in json.flaggedTokens)
                {
                    text = text.Replace(flaggedToken.token, flaggedToken.suggestions.FirstOrDefault().suggestion);
                }

                return text;
            }

            return text;
        }
    }
}
