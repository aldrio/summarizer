class Summarizer(object):
    """Abstract summarizer"""

    def summarize(self, paragraphs: list[list[str]]) -> list[list[str]]:
        """
        Summarize content

        :param content: List of paragraphs, each paragraph is a list of sentences
        """
        raise NotImplementedError()

    def summarize_article(self, paragraphs: list[list[str]]) -> list[list[str]]:
        """
        Summarize an article

        :param content: List of paragraphs, each paragraph is a list of sentences
        """
        return self.summarize(paragraphs)

    def summarize_video(self, subs: list[str]) -> list[str]:
        """
        Summarize a video

        :param content: List of sentences (subtitles)
        """

        summarized = self.summarize([subs])
        if not summarized:
            return []
        else:
            assert len(summarized) == 1
            return summarized[0]

    def algorithm_name(self):
        """Return the name of the algorithm"""

        raise NotImplementedError()

    def supports_malformed(self):
        """Return whether the summarizer supports malformed content"""

        return False
