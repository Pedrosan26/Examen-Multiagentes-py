from Calle import Calle
from Agente import Agente
import agentpy as ap

class RouteModel(ap.Model):
    def setup(self):
        self.simulation_complete = False
        self.current_path = None
        self.env = Calle(self, shape=self.p.streets.shape)
        self.agent = Agente(self)
        self.env.add_agents([self.agent], positions=[self.p.start])

    def step(self):
        if not self.simulation_complete:
            result = self.agent.execute()
            if result is None:
                self.simulation_complete = True
                self.stop()