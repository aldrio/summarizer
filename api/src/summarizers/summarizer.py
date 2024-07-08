class Summarizer(object):
    """Abstract summarizer"""

    def summarize(self, paragraphs: list[list[str]]) -> list[str]:
        """Summarize a document"""

        raise NotImplementedError()

    def algorithm_name(self):
        """Return the name of the algorithm"""

        raise NotImplementedError()

    def supports_malformed(self):
        """Return whether the summarizer supports malformed content"""

        return False
