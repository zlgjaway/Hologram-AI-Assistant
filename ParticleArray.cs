using UnityEngine;

public class ParticleArray  : MonoBehaviour {

    public Transform particlePrefab;

    public int arraySize  = 10;

    Transform[] grid;

    void Awake () {
        grid = new Transform[arraySize  * arraySize ];
        for (int i = 0, x = 0; x < arraySize ; ++x) {
            for (int z = 0; z < arraySize ; z++, i++) {
                grid[i] = CreateGridPoint(x, z);
            }
        }
    }

    Transform CreateGridPoint (int x, int z) {
        Transform point = Instantiate<Transform>(particlePrefab);
        point.localPosition = GetCoordinates(x, z);
        point.GetComponent<ParticleSystemRenderer>().material.color = new Color(
            (float)x / arraySize ,
            0.5f, // Example fixed value for y-axis color component
            (float)z / arraySize 
        );
        return point;
    }

    Vector3 GetCoordinates (int x, int z) {
        return new Vector3(
            x-(arraySize  - 1) * 0.5f,
            0, // Example fixed value for y-coordinate
            z-(arraySize  - 1) * 0.5f
            
        );
    }

}
