using UnityEngine;

public class EmissionController : MonoBehaviour
{
    public Color emissionColor = Color.red;
    public float emissionIntensity = 1.0f;

    Renderer rend;
    Material mat;

    void Start()
    {
        rend = GetComponent<Renderer>();
        mat = rend.material;
    }

    void Update()
    {
        // Example: Change emission color and intensity over time
        float emission = Mathf.PingPong(Time.time, 1.0f); // Example of varying emission intensity

        // Set emission color and intensity
        mat.SetColor("_EmissionColor", emissionColor * emissionIntensity * emission);
        mat.SetFloat("_EmissionIntensity", emissionIntensity); // Optional: set a float for intensity if not using color

        // Enable emission keyword if necessary (ensure your shader supports _EMISSION keyword)
        if (emission > 0)
        {
            mat.EnableKeyword("_EMISSION");
        }
        else
        {
            mat.DisableKeyword("_EMISSION");
        }
    }
}
