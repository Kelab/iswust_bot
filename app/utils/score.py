from typing import TYPE_CHECKING

import pandas as pd

from app.models.score import CETScore, PhysicalOrCommonScore, PlanScore, ScoreCata

if TYPE_CHECKING:
    from app.utils.parse.score import ScoreDict


async def save_score(user, score: ScoreDict):
    await CETScore.add_or_update(user.student_id, score["cet"])
    await PhysicalOrCommonScore.add_or_update(user.student_id, score, ScoreCata.COMMON)
    await PhysicalOrCommonScore.add_or_update(
        user.student_id, score, ScoreCata.PHYSICAL
    )
    await PlanScore.add_or_update(user.student_id, score["plan"])


def diff(new, old) -> pd.DataFrame:
    result = []
    for idx, n_series in new.iterrows():
        flag = 0
        for _, o_series in old.iterrows():
            if (
                n_series["课程号"] == o_series["课程号"]
                and n_series["term"] == o_series["term"]
                and n_series["season"] == o_series["season"]
            ):
                flag = 1
                break
        if flag == 0:
            result.append(idx)
    df = new.iloc[result]
    return df
