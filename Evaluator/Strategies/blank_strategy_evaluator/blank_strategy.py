#  Drakkar-Software OctoBot-Tentacles
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import octobot_evaluators.evaluators as evaluators
import octobot_evaluators.enums as enums


class BlankStrategyEvaluator(evaluators.StrategyEvaluator):

    def get_full_cycle_evaluator_types(self) -> tuple:
        # returns a tuple as it is faster to create than a list
        return enums.EvaluatorMatrixTypes.TA.value, enums.EvaluatorMatrixTypes.SCRIPTED.value

    async def matrix_callback(self,
                              matrix_id,
                              evaluator_name,
                              evaluator_type,
                              eval_note,
                              eval_note_type,
                              exchange_name,
                              cryptocurrency,
                              symbol,
                              time_frame):
        self.eval_note = eval_note
        await self.strategy_completed(cryptocurrency, symbol, time_frame=time_frame)
