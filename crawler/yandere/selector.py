def safe_selector(picture_info):
    """
    Picture with safe rating passes this test.
    """
    return picture_info['rating'] == 'Safe'


def score_selector_factory(score_threshold):
    """
    Produce a selector to pick up picture scoring higer than specified
    threshold.
    """
    def score_seletor(picture_info):
        return picture_info['score'] >= score_threshold
    return score_seletor
