using UnityEngine;
using System.Collections;

namespace RogueProject2.Controllers
{
    /// <summary>
    /// Unity C# Skill System for Duran Paladin V6
    /// Skills: Q (Holy Slash), W (Holy Shield), E (Consecration), R (Angel Blade), Space (Divine Intervention)
    /// </summary>
    public class SkillSystem : MonoBehaviour
    {
        private PlayerController2D player;

        [Header("Skill Prefabs & Effects")]
        public GameObject holySlashFxPrefab;
        public GameObject holyShieldFxPrefab;
        public GameObject consecrationFxPrefab;
        public GameObject angelBladeProjectilePrefab;
        public GameObject divineInterventionFxPrefab;

        private void Awake()
        {
            player = GetComponent<PlayerController2D>();
        }

        private void Update()
        {
            if (Input.GetKeyDown(KeyCode.Q) || Input.GetKeyDown(KeyCode.Space))
            {
                CastHolySlash();
            }
            if (Input.GetKeyDown(KeyCode.W))
            {
                CastHolyShield();
            }
            if (Input.GetKeyDown(KeyCode.E))
            {
                CastConsecration();
            }
            if (Input.GetKeyDown(KeyCode.R))
            {
                CastAngelBlade();
            }
        }

        public void CastHolySlash()
        {
            Vector2 dir = player.GetFacingDirection();
            Vector3 spawnPos = transform.position + new Vector3(dir.x, dir.y, 0) * 1.2f;

            Debug.Log("⚔️ 스킬 1: 성스러운 베기 (Holy Slash) 시전!");
            player.AddSP(10f);

            // Hit Detection in OverlapCircle
            Collider2D[] hits = Physics2D.OverlapCircleAll(spawnPos, 1.5f);
            foreach (var hit in hits)
            {
                if (hit.CompareTag("Monster"))
                {
                    MonsterAI monster = hit.GetComponent<MonsterAI>();
                    if (monster != null)
                    {
                        monster.TakeDamage(player.attackPower + Random.Range(0, 15));
                    }
                }
            }
        }

        public void CastHolyShield()
        {
            if (player.currentMp >= 15)
            {
                player.currentMp -= 15;
                Debug.Log("🛡️ 스킬 2: 신성한 방패 (Holy Shield) 전개!");
                player.isInvincible = true;
                StartCoroutine(ShieldTimerRoutine(4.0f));
            }
        }

        private IEnumerator ShieldTimerRoutine(float duration)
        {
            yield return new WaitForSeconds(duration);
            player.isInvincible = false;
        }

        public void CastConsecration()
        {
            if (player.currentMp >= 20)
            {
                player.currentMp -= 20;
                Debug.Log("✨ 스킬 3: 축성 (Consecration) 마법진 생성!");
            }
        }

        public void CastAngelBlade()
        {
            if (player.currentMp >= 25)
            {
                player.currentMp -= 25;
                Debug.Log("👼 스킬 4: 천사의 검 (Angel Blade) 발사!");
            }
        }

        public void CastDivineIntervention()
        {
            if (player.currentSp >= player.maxSp)
            {
                player.currentSp = 0;
                Debug.Log("🌟 필살기: 신성한 개입 (Divine Intervention) 3단계 발동!");
            }
        }
    }
}
