// ------------------------------------------------------------------------------
// <copyright file="SpellCheckSchema.cs">
//   Object Representation of the JSON returned by the Bing Spell Check API
// </copyright>
// ------------------------------------------------------------------------------

using System.Collections.Generic;

public class Suggestion
{
    public string suggestion { get; set; }
    public double score { get; set; }
}

public class FlaggedToken
{
    public int offset { get; set; }
    public string token { get; set; }
    public string type { get; set; }
    public List<Suggestion> suggestions { get; set; }
}

public class RootObject
{
    public string _type { get; set; }
    public List<FlaggedToken> flaggedTokens { get; set; }
}
