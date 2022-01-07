import datetime
from diff_match_patch import diff_match_patch


class ArticleVersion:
    #loads arguments into variables
    def __init__(self, dictionary):
        self.datetime = dictionary.get("datetime") or datetime.datetime.utcnow()
        self.headline = dictionary.get("headline")
        self.subhead = dictionary.get("subhead")
        self.byline = dictionary.get("byline")
        self.content = dictionary.get("content")

    #gets relative difference to last version
    def get_similarity(self, other):
        weights = {"headline": 0.2, "subhead": 0.1, "byline": 0.1, "content": 0.6}
        total_similarity = 0
        similarities = {"headline": 0, "subhead": 0, "byline": 0, "content": 0}
        self_vars = vars(self)
        other_vars = vars(other)
        for key in weights:
            #if they're exactly the same, set to 1 and continue
            if self_vars[key] == other_vars[key]:
                total_similarity += weights[key]
                similarities[key] = 1
                continue
            #if either one of them is falsy then set to zero
            if not self_vars[key] or not other_vars[key]:
                continue
            #diff the parts
            dmp = diff_match_patch()
            diff = dmp.diff_main(self_vars[key], other_vars[key])
            # first part is how much of the text is shared, second part is total length
            similarity = sum(
                [len(text) for operation, text in diff if operation == 0]
            ) / max(len(self_vars[key]), len(other_vars[key]))
            similarities[key] = similarity
            total_similarity += weights[key] * similarity
        #returns stuff
        return total_similarity, similarities

    #defines equality to ignore time/similarities
    def __eq__(self, other):
        if isinstance(other, ArticleVersion):
            return (
                (self.headline == other.headline)
                and (self.subhead == other.subhead)
                and (self.byline == other.byline)
                and (self.content == other.content)
            )
        return False
