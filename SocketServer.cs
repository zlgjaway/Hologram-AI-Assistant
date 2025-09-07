using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Collections;
using UnityEngine.UI;
using Newtonsoft.Json;
using System.IO;
public class WeatherData
{
    public double latitude { get; set; }
    public double longitude { get; set; }
    public CurrentWeather current_weather { get; set; }
    public Daily daily { get; set; }

    public class CurrentWeather
    {
        public double temperature { get; set; }
        public int weathercode { get; set; }
    }

    public class Daily
    {
        public List<double> uv_index_max { get; set; }
    }
}

public class SocketServer: MonoBehaviour
{
    private TcpListener server;
    private ConcurrentQueue<string> messageQueue = new ConcurrentQueue<string>();
    private Thread serverThread;
    public int port = 8080;
    public Animator[] myAnimators;
    public GameObject canvas;
    public GameObject panel;
    public GameObject panel2;
    public GameObject panel3;
    public Text temperatureText;
    public Text temperatureText2;
    public Text temperatureText3;
    public Text uvIndexText;
    public Text uvIndexText2;
    public Text uvIndexText3;
    public Image weatherIcon; // Add this to show the weather icon
    public Image weatherIcon2; // Add this to show the weather icon2
    public Image weatherIcon3; // Add this to show the weather icon3
    public Sprite[] weatherIcons; // Array to hold different weather icons

    void Start()
    {
        // Ensure panel and UI elements are assigned
        if (panel == null || temperatureText == null || uvIndexText == null || weatherIcon == null || weatherIcons == null || weatherIcons.Length == 0)
        {
            Debug.LogError("One or more UI elements are not assigned in the Inspector.");
            return;
        }

        serverThread = new Thread(new ThreadStart(ServerStart));
        serverThread.IsBackground = true;
        serverThread.Start();
        panel.SetActive(false);
        panel2.SetActive(false);
        panel3.SetActive(false);
        canvas.SetActive(false);

    }
    IEnumerator ActivatePanelAfterDelay(float delay)
    {
        yield return new WaitForSeconds(delay);
        panel.SetActive(true);
        panel2.SetActive(true);
        panel3.SetActive(true);
        canvas.SetActive(true);
    }

    void Update()
    {
        string filePath = Path.Combine(Application.dataPath, "D:\\My project\\weather.json");

        // Retry mechanism
        int maxRetries = 5;
        int delayMilliseconds = 10;

        for (int i = 0; i < maxRetries; i++)
        {
            try
            {
                if (File.Exists(filePath))
                {
                    // Open the file with shared read access
                    using (FileStream fs = new FileStream(filePath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
                    using (StreamReader sr = new StreamReader(fs))
                    {
                        string json = sr.ReadToEnd();
                        WeatherData weatherData = JsonConvert.DeserializeObject<WeatherData>(json);

                    // Process messages on the main thread
                        while (messageQueue.TryDequeue(out string message))
                        {
                            ProcessMessage(message, weatherData);
                        }
                    }
                }
                else
                {
                    Debug.LogError($"File not found at path: {filePath}");
                }

                // Exit the retry loop if successful
                break;
            }
            catch (IOException ex)
            {
                Debug.LogWarning($"IOException: {ex.Message}. Retrying in {delayMilliseconds}ms...");

                // Wait before retrying
                Thread.Sleep(delayMilliseconds);
            }
        }
    }

    void ServerStart()
    {
        try
        {
            server = new TcpListener(IPAddress.Any, port);
            server.Start();
            Debug.Log("Server started on port " + port);

            while (true)
            {
                using (TcpClient client = server.AcceptTcpClient())
                {
                    using (NetworkStream stream = client.GetStream())
                    {
                        byte[] buffer = new byte[1024];
                        int bytesRead = stream.Read(buffer, 0, buffer.Length);
                        string message = Encoding.UTF8.GetString(buffer, 0, bytesRead);

                        // Queue the message to be processed on the main thread
                        messageQueue.Enqueue(message);
                    }
                }
            }
        }
        catch (Exception e)
        {
            Debug.LogError("Socket error: " + e.Message);
        }
    }
    

    private void ProcessMessage(string message, WeatherData weatherData)
    {
        Debug.Log($"Received message: {message}");
        switch (message)
        {
            case "Triger random Action 1":
                TrigerrandomAction1();
                break;
            case "Triger forecast":
                Triger_forecast();
                DisplayWeatherData(weatherData);
                break;
            case "untriger forecast":
                unTriger_forecast();
                break;
            default:
                Debug.LogWarning($"Unknown message: {message}");
                break;
        }
    }

    private void TrigerrandomAction1()
    {
        foreach (Animator animator in myAnimators)
        {
            animator.SetTrigger("Triger random Action 1");
        }
        Debug.Log("Action 1 animation triggered.");
    }

    private void Triger_forecast()
    {
         Debug.Log("Triggering forecast animation...");
        foreach (Animator animator in myAnimators)
        {
            animator.SetTrigger("Triger forecast ");
        }
    }

    private void unTriger_forecast()
    {   
        canvas.SetActive(false);
        panel.SetActive(false); // Hide the panel
        panel2.SetActive(false);// Hide the panel
        panel3.SetActive(false);// Hide the panel

        foreach (Animator animator in myAnimators)
        {
            animator.SetTrigger("untriger forecast");
        }
        Debug.Log("forecast animation untriggerd.");
    }


    private void DisplayWeatherData(WeatherData weatherData)
    {
        if (weatherData == null)
        {
            Debug.LogError("Weather data is null!");
            return;
        }

        StartCoroutine(ActivatePanelAfterDelay(2.06f));
        temperatureText.text = $"{weatherData.current_weather.temperature}°C";
        temperatureText2.text = $"{weatherData.current_weather.temperature}°C";
        temperatureText3.text = $"{weatherData.current_weather.temperature}°C";
        uvIndexText.text = $"UV Index: {weatherData.daily.uv_index_max[0]}";
        uvIndexText2.text = $"UV Index: {weatherData.daily.uv_index_max[0]}";
        uvIndexText3.text = $"UV Index: {weatherData.daily.uv_index_max[0]}";



        // Set the weather icon based on the weather code
        weatherIcon.sprite = GetWeatherIcon(weatherData.current_weather.weathercode);
        weatherIcon2.sprite = GetWeatherIcon(weatherData.current_weather.weathercode);
        weatherIcon3.sprite = GetWeatherIcon(weatherData.current_weather.weathercode);
    }
   

    private Sprite GetWeatherIcon(int weatherCode)
    {
        if (weatherIcons == null || weatherIcons.Length == 0)
        {
            Debug.LogError("Weather icons are not assigned or empty.");
            return null;
        }

        // Map weather codes to appropriate icons
        switch (weatherCode)
        {
            case 0:
                return weatherIcons[0]; // Clear sky icon
            case 1:
                return weatherIcons[1]; // Partly cloudy icon
            // Add more cases for different weather codes
            case 2:
                return weatherIcons[2]; // Rain icon
            case 3:
                return weatherIcons[3]; // Thunderstorm icon
            default:
                return weatherIcons[0];              
        }
    }

    

    void OnApplicationQuit()
    {
        if (server != null)
        {
            server.Stop();
        }
        if (serverThread != null)
        {
            serverThread.Abort();
        }
    }
}
