using UnityEngine;

namespace RogueProject2.Core
{
    /// <summary>
    /// Unity 6 Master Singleton Game Manager for Infinite Sword: Infinite Dungeon
    /// </summary>
    public class GameManager : MonoBehaviour
    {
        public static GameManager Instance { get; private set; }

        public enum GameState { Title, InGame, HubShop, GameOver }

        [Header("Master Game State")]
        public GameState currentState = GameState.Title;
        public int floor = 1;
        public int kills = 0;
        public int gold = 0;

        private void Awake()
        {
            if (Instance == null)
            {
                Instance = this;
                DontDestroyOnLoad(gameObject);
            }
            else
            {
                Destroy(gameObject);
            }
        }

        public void ChangeState(GameState newState)
        {
            currentState = newState;
            Debug.Log($"🎮 [Unity GameManager] State Changed to: {newState}");
        }

        public void AddGold(int amount)
        {
            gold += amount;
        }

        public void AddKill()
        {
            kills++;
        }
    }
}
