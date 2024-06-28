using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEditor.VersionControl;
using UnityEngine;
using System.Collections.Concurrent;

public class SocketServer : MonoBehaviour
{
    private TcpListener server;
    private ConcurrentQueue<string> messageQueue = new ConcurrentQueue<string>();
    private Thread serverThread;
    public int port = 8080;
   public Animator[] myAnimators;

    void Start()
    {
        serverThread = new Thread(new ThreadStart(ServerStart));
        serverThread.IsBackground = true;
        serverThread.Start();
        //myAnimators =  GetComponent<Animator[]>();
        foreach (Animator animator in myAnimators)
        {
            GetComponent<Animator>();
        }
    }


      void Update()
    {

        // Process messages on the main thread
          while (messageQueue.TryDequeue(out string message))
        {
            ProcessMessage(message);
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

    private void ProcessMessage(string message)
    {
        Debug.Log($"Received message: {message}");
        switch (message)
        {
            case "Triger Action 1":
               TrigerrandomAction1();
                break;
            default:
                Debug.LogWarning($"Unknown message: {message}");
                break;
        }
    } 

    private void TrigerrandomAction1()
    {
        // Trigger the idle animation
        //myAnimators.SetTrigger("Triger random Action 1");
        foreach (Animator animator in myAnimators)
        {
            animator.SetTrigger("Triger random Action 1");
        }
        Debug.Log("Action 1 animation triggered.");
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

