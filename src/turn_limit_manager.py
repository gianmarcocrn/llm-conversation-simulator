import autogen

class TurnLimitManager:
    def __init__(self, max_turns, user_proxy: autogen.UserProxyAgent):
        self.turns = 0
        self.max_turns = max_turns
        self.user_proxy = user_proxy

    def _is_termination_by_proxy(self, msg):
        return self.turns >= self.max_turns

    def is_termination_by_agents(self, msg):
        self.turns += 1
        self.user_proxy._is_termination_msg = self._is_termination_by_proxy
        if self.turns >= (self.max_turns - 2):
            print("FINAL TURNS")
            self.user_proxy._default_auto_reply = "Resolve any open conversation topics and then wrap up the conversation."
        if (self.turns > self.max_turns): print("FINISHING CONVERSATION")
        return self.turns > self.max_turns