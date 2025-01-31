using UnityEngine;
using System.Collections;
using UnityEngine.Networking;

public class HttpClient : MonoBehaviour {
    void Start() {
        StartCoroutine(GetAgentData());
    }

    IEnumerator GetAgentData() {
        string url = "http://localhost:10000/agente";
        
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url)) {
            yield return webRequest.SendWebRequest();

            if (webRequest.result == UnityWebRequest.Result.ConnectionError || 
                webRequest.result == UnityWebRequest.Result.ProtocolError) {
                Debug.LogError("Error: " + webRequest.error);
            }
            else {
                // Imprimir todo el JSON en consola
                Debug.Log("Datos recibidos:\n" + webRequest.downloadHandler.text);
                
                // Opcional: Parsear el JSON
                ProcessJsonData(webRequest.downloadHandler.text);
            }
        }
    }

    void ProcessJsonData(string json) {
        try {
            AgentData data = JsonUtility.FromJson<AgentData>(json);
            Debug.Log($"Datos procesados - Costo total: {data.metadata.total_cost}");
        }
        catch (System.Exception e) {
            Debug.LogError("Error al parsear JSON: " + e.Message);
        }
    }

    // Clases para deserialización
    [System.Serializable]
    public class AgentData {
        public MapData map;
        public PathStep[] path;
        public Metadata metadata;
    }

    [System.Serializable]
    public class MapData {
        public int[] dimensions;
        public int[] start;
        public int[] goal;
        public string[][] terrain_grid;
    }

    [System.Serializable]
    public class PathStep {
        public int step;
        public int[] position;
        public string terrain;
        public float cost;
        public string type;
    }

    [System.Serializable]
    public class Metadata {
        public float total_cost;
        public int path_length;
        public string algorithm;
    }
}