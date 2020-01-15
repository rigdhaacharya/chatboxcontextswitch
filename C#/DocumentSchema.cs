// ------------------------------------------------------------------------------
// <copyright file="DocumentSchema.cs">
//   Object Representation of the Maluuba frames JSON data
// </copyright>
// ------------------------------------------------------------------------------

namespace ParseFrames
{
    using System.Collections.Generic;

    public class Act
    {
        public List<object> args { get; set; }
        public string name { get; set; }
    }

    public class ActsWithoutRef
    {
        public List<object> args { get; set; }
        public string name { get; set; }
    }

    public class Intent
    {
        public string val { get; set; }
        public bool negated { get; set; }
    }

    public class Budget
    {
        public string val { get; set; }
        public bool negated { get; set; }
    }

    public class DstCity
    {
        public string val { get; set; }
        public bool negated { get; set; }
    }

    public class OrCity
    {
        public string val { get; set; }
        public bool negated { get; set; }
    }

    public class StrDate
    {
        public string val { get; set; }
        public bool negated { get; set; }
    }

    public class NAdult
    {
        public string val { get; set; }
        public bool negated { get; set; }
    }

    public class NORESULT
    {
        public bool val { get; set; }
        public bool negated { get; set; }
    }

    public class Flex
    {
        public bool val { get; set; }
        public bool negated { get; set; }
    }

    public class Info
    {
        public List<Intent> intent { get; set; }
        public List<Budget> budget { get; set; }
        public List<DstCity> dst_city { get; set; }
        public List<OrCity> or_city { get; set; }
        public List<StrDate> str_date { get; set; }
        public List<NAdult> n_adults { get; set; }
        public List<NORESULT> NO_RESULT { get; set; }
        public List<Flex> flex { get; set; }
    }

    public class Frame
    {
        public Info info { get; set; }
        public int frame_id { get; set; }
        public List<object> requests { get; set; }
        public int? frame_parent_id { get; set; }
        public List<object> binary_questions { get; set; }
        public List<object> compare_requests { get; set; }
    }

    public class Labels
    {
        public List<Act> acts { get; set; }
        public List<ActsWithoutRef> acts_without_refs { get; set; }
        public int active_frame { get; set; }
        public List<Frame> frames { get; set; }
    }

    public class Search
    {
        public string ORIGIN_CITY { get; set; }
        public string PRICE_MIN { get; set; }
        public string NUM_ADULTS { get; set; }
        public double timestamp { get; set; }
        public string PRICE_MAX { get; set; }
        public string ARE_DATES_FLEXIBLE { get; set; }
        public string NUM_CHILDREN { get; set; }
        public string START_TIME { get; set; }
        public double MAX_DURATION { get; set; }
        public string DESTINATION_CITY { get; set; }
        public string RESULT_LIMIT { get; set; }
        public string END_TIME { get; set; }
    }

    public class Db
    {
        public List<List<object>> result { get; set; }
        public List<Search> search { get; set; }
    }

    public class Turn
    {
        public string text { get; set; }
        public Labels labels { get; set; }
        public string author { get; set; }
        public double timestamp { get; set; }
        public Db db { get; set; }
    }

    public class Labels2
    {
        public double? userSurveyRating { get; set; }
        public bool wizardSurveyTaskSuccessful { get; set; }
    }

    public class RootObject
    {
        public string user_id { get; set; }
        public List<Turn> turns { get; set; }
        public string wizard_id { get; set; }
        public string id { get; set; }
        public Labels2 labels { get; set; }
    }
}
