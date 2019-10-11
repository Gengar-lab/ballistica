# Copyright (c) 2011-2019 Eric Froemling
"""Functionality related to the end screen in dual-team mode."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
from bastd.activity.teamsscorescreen import TeamsScoreScreenActivity
from bastd.actor.zoomtext import ZoomText

if TYPE_CHECKING:
    from typing import Any, Dict


class TeamVictoryScoreScreenActivity(TeamsScoreScreenActivity):
    """Scorescreen between rounds of a dual-team session."""

    def __init__(self, settings: Dict[str, Any]):
        super().__init__(settings=settings)

    # noinspection PyMethodOverriding
    def on_begin(self) -> None:  # type: ignore
        # FIXME: Unify args.
        # pylint: disable=arguments-differ
        from ba.deprecated import get_resource
        ba.set_analytics_screen('Teams Score Screen')
        super().on_begin()

        height = 130
        active_team_count = len(self.teams)
        vval = (height * active_team_count) / 2 - height / 2
        i = 0
        shift_time = 2.5

        # Usually we say 'Best of 7', but if the language prefers we can say
        # 'First to 4'.
        session = self.session
        assert isinstance(session, ba.TeamBaseSession)
        if get_resource('bestOfUseFirstToInstead'):
            best_txt = ba.Lstr(resource='firstToSeriesText',
                               subs=[('${COUNT}',
                                      str(session.get_series_length() / 2 + 1))
                                     ])
        else:
            best_txt = ba.Lstr(resource='bestOfSeriesText',
                               subs=[('${COUNT}',
                                      str(session.get_series_length()))])

        ZoomText(best_txt,
                 position=(0, 175),
                 shiftposition=(-250, 175),
                 shiftdelay=2.5,
                 flash=False,
                 trail=False,
                 h_align='center',
                 scale=0.25,
                 color=(0.5, 0.5, 0.5, 1.0),
                 jitter=3.0).autoretain()
        for team in self.teams:
            ba.timer(
                i * 0.15 + 0.15,
                ba.WeakCall(self._show_team_name, vval - i * height, team,
                            i * 0.2, shift_time - (i * 0.150 + 0.150)))
            ba.timer(i * 0.150 + 0.5,
                     ba.Call(ba.playsound, self._score_display_sound_small))
            scored = (team is self.settings['winner'])
            delay = 0.2
            if scored:
                delay = 1.2
                ba.timer(
                    i * 0.150 + 0.2,
                    ba.WeakCall(self._show_team_old_score, vval - i * height,
                                team, shift_time - (i * 0.15 + 0.2)))
                ba.timer(i * 0.15 + 1.5,
                         ba.Call(ba.playsound, self._score_display_sound))

            ba.timer(
                i * 0.150 + delay,
                ba.WeakCall(self._show_team_score, vval - i * height, team,
                            scored, i * 0.2 + 0.1,
                            shift_time - (i * 0.15 + delay)))
            i += 1
        self.show_player_scores()

    def _show_team_name(self, pos_v: float, team: ba.Team, kill_delay: float,
                        shiftdelay: float) -> None:
        del kill_delay  # unused arg
        ZoomText(ba.Lstr(value='${A}:', subs=[('${A}', team.name)]),
                 position=(100, pos_v),
                 shiftposition=(-150, pos_v),
                 shiftdelay=shiftdelay,
                 flash=False,
                 trail=False,
                 h_align='right',
                 maxwidth=300,
                 color=team.color,
                 jitter=1.0).autoretain()

    def _show_team_old_score(self, pos_v: float, team: ba.Team,
                             shiftdelay: float) -> None:
        ZoomText(str(team.sessiondata['score'] - 1),
                 position=(150, pos_v),
                 maxwidth=100,
                 color=(0.6, 0.6, 0.7),
                 shiftposition=(-100, pos_v),
                 shiftdelay=shiftdelay,
                 flash=False,
                 trail=False,
                 lifespan=1.0,
                 h_align='left',
                 jitter=1.0).autoretain()

    def _show_team_score(self, pos_v: float, team: ba.Team, scored: bool,
                         kill_delay: float, shiftdelay: float) -> None:
        del kill_delay  # unused arg
        ZoomText(str(team.sessiondata['score']),
                 position=(150, pos_v),
                 maxwidth=100,
                 color=(1.0, 0.9, 0.5) if scored else (0.6, 0.6, 0.7),
                 shiftposition=(-100, pos_v),
                 shiftdelay=shiftdelay,
                 flash=scored,
                 trail=scored,
                 h_align='left',
                 jitter=1.0,
                 trailcolor=(1, 0.8, 0.0, 0)).autoretain()
