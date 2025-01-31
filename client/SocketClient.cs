using UnityEngine;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class SocketClient : MonoBehaviour {
    TcpClient client;
    NetworkStream stream;
    Thread receiveThread;
    bool isConnected = false;
    
    void Start() {
        ConnectToServer("localhost", 65432);
    }

    void ConnectToServer(string host, int port) {
        try {
            client = new TcpClient(host, port);
            stream = client.GetStream();
            isConnected = true;
            receiveThread = new Thread(new ThreadStart(ReceiveData));
            receiveThread.Start();
        } catch (System.Exception e) {
            Debug.LogError("Error de conexión: " + e.Message);
        }
    }

    void ReceiveData() {
        byte[] buffer = new byte[1024];
        while (isConnected) {
            try {
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                string jsonData = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                ProcessData(jsonData);
            } catch {
                break;
            }
        }
    }

    void ProcessData(string json) {
        // Parsear JSON y actualizar la simulación en Unity
        Debug.Log("Datos recibidos: " + json);
        
        // Ejemplo de cómo podrías manejar los datos:
        /* var data = JsonUtility.FromJson<SimulationData>(json);
        switch (data.type) {
            case "simulation_start":
                InitializeTerrain(data.map_data);
                break;
            case "step_update":
                MoveAgent(data.current_position);
                UpdateUI(data.current_cost);
                break;
            case "simulation_end":
                ShowFinalResults(data.total_cost);
                break;
        } */
    }

    void OnDestroy() {
        isConnected = false;
        if (stream != null) stream.Close();
        if (client != null) client.Close();
    }
}