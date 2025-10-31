import pytest

from pdfdrive_api.extras import ExtraRecommendedBook, Extras

extras = Extras()


@pytest.mark.asyncio
async def test_recommended_book():
    recommendations = await extras.recommend("rich")
    for rec in recommendations:
        assert isinstance(rec, ExtraRecommendedBook)
