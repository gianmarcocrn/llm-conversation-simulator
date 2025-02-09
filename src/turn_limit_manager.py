import autogen

class TurnLimitManager:
    def __init__(self, max_turns, user_proxy: autogen.UserProxyAgent):
        self.turns = 0
        self.max_turns = max_turns
        self.user_proxy = user_proxy

    def _is_termination_by_proxy(self, msg):
        print("is_termination_by_proxy evaluates to: " + str(self.turns >= self.max_turns))
        if (self.turns >= self.max_turns): print("CONVERSATION FINISHED")
        return self.turns >= self.max_turns

    def is_termination_by_agents(self, msg):
        self.turns += 1
        self.user_proxy._is_termination_msg = self._is_termination_by_proxy
        print(f"Turns so far: {self.turns}, Max turns: {self.max_turns}")
        if self.turns >= (self.max_turns - 2):
            self.user_proxy._default_auto_reply = "Resolve any open conversation topics and do not introduce new ones. Then wrap up the conversation."
        print("is_termination_by_agent evaluates to: " + str(self.turns > self.max_turns))
        if (self.turns > self.max_turns): print("CONVERSATION FINISHED")
        return self.turns > self.max_turns