using UnityEngine;
using System.Collections.Generic;

namespace RogueProject2.Managers
{
    /// <summary>
    /// Unity Dungeon Manager for Stage Themes (1~10), Floor Navigation, and Spawns
    /// </summary>
    public class DungeonManager : MonoBehaviour
    {
        public static DungeonManager Instance { get; private set; }

        [System.Serializable]
        public struct StageTheme
        {
            public int stageId;
            public string stageName;
            public Color backgroundColor;
            public GameObject bossPrefab;
        }

        [Header("Dungeon Progress")]
        public int currentFloor = 1;
        public int currentStageIndex = 0;
        public int totalKills = 0;

        [Header("Stage Themes Database")]
        public List<StageTheme> stageThemes = new List<StageTheme>();

        [Header("Prefabs Database")]
        public List<GameObject> monsterPrefabs = new List<GameObject>();
        public Transform[] spawnPoints;

        private void Awake()
        {
            if (Instance == null) Instance = this;
            else Destroy(gameObject);
        }

        private void Start()
        {
            LoadStage(currentStageIndex);
        }

        public void LoadStage(int index)
        {
            currentStageIndex = index % stageThemes.Count;
            StageTheme currentTheme = stageThemes[currentStageIndex];

            Debug.Log($"🗺️ [Unity Dungeon] Stage {currentFloor}: {currentTheme.stageName} 로드 완료!");
            Camera.main.backgroundColor = currentTheme.backgroundColor;

            SpawnWave();
        }

        public void SpawnWave()
        {
            int monsterCount = 6 + currentFloor * 2;
            Debug.Log($"👾 {monsterCount}마리 몬스터 스폰 완료");
        }

        public void OnMonsterKilled()
        {
            totalKills++;
            // Check if floor cleared
        }
    }
}
