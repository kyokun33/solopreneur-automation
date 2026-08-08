using UnityEngine;

namespace RogueProject2.Controllers
{
    /// <summary>
    /// Unity 2D Monster AI for Regular Monsters & Bosses
    /// FSM States: Idle, Chase, Attack, HitStun, Dead
    /// </summary>
    [RequireComponent(typeof(Rigidbody2D))]
    public class MonsterAI : MonoBehaviour
    {
        public enum MonsterState { Idle, Chase, Attack, HitStun, Dead }

        [Header("Monster Stats")]
        public string monsterName = "버섯 몬스터";
        public int currentHp = 50;
        public int maxHp = 50;
        public int attackDamage = 10;
        public float moveSpeed = 2.5f;
        public float chaseRadius = 8.0f;
        public float attackRadius = 1.2f;
        public bool isBoss = false;

        [Header("FSM State")]
        public MonsterState currentState = MonsterState.Idle;

        private Transform playerTransform;
        private Rigidbody2D rb;
        private float attackCooldownTimer = 0f;
        private float hitStunTimer = 0f;

        private void Awake()
        {
            rb = GetComponent<Rigidbody2D>();
            rb.gravityScale = 0f;
            rb.freezeRotation = true;
        }

        private void Start()
        {
            GameObject pObj = GameObject.FindWithTag("Player");
            if (pObj != null) playerTransform = pObj.transform;
        }

        private void Update()
        {
            if (currentState == MonsterState.Dead) return;

            HandleTimers();
            FSMUpdate();
        }

        private void FSMUpdate()
        {
            if (playerTransform == null) return;

            float distToPlayer = Vector2.Distance(transform.position, playerTransform.position);

            switch (currentState)
            {
                case MonsterState.Idle:
                    if (distToPlayer <= chaseRadius) currentState = MonsterState.Chase;
                    rb.velocity = Vector2.zero;
                    break;

                case MonsterState.Chase:
                    if (distToPlayer <= attackRadius)
                    {
                        currentState = MonsterState.Attack;
                    }
                    else if (distToPlayer > chaseRadius * 1.5f)
                    {
                        currentState = MonsterState.Idle;
                    }
                    else
                    {
                        Vector2 dir = (playerTransform.position - transform.position).normalized;
                        rb.velocity = dir * moveSpeed;
                    }
                    break;

                case MonsterState.Attack:
                    rb.velocity = Vector2.zero;
                    if (attackCooldownTimer <= 0f)
                    {
                        PerformAttack();
                    }
                    if (distToPlayer > attackRadius)
                    {
                        currentState = MonsterState.Chase;
                    }
                    break;

                case MonsterState.HitStun:
                    rb.velocity = Vector2.zero;
                    if (hitStunTimer <= 0f)
                    {
                        currentState = MonsterState.Chase;
                    }
                    break;
            }
        }

        private void PerformAttack()
        {
            attackCooldownTimer = isBoss ? 2.0f : 1.5f;
            if (playerTransform != null)
            {
                PlayerController2D player = playerTransform.GetComponent<PlayerController2D>();
                if (player != null)
                {
                    player.TakeDamage(attackDamage);
                }
            }
        }

        private void HandleTimers()
        {
            if (attackCooldownTimer > 0f) attackCooldownTimer -= Time.deltaTime;
            if (hitStunTimer > 0f) hitStunTimer -= Time.deltaTime;
        }

        public void TakeDamage(int damage)
        {
            if (currentState == MonsterState.Dead) return;

            currentHp -= damage;
            currentState = MonsterState.HitStun;
            hitStunTimer = 0.3f; // 0.3s Hit Stun

            if (currentHp <= 0)
            {
                Die();
            }
        }

        private void Die()
        {
            currentState = MonsterState.Dead;
            rb.velocity = Vector2.zero;
            Debug.Log($"💀 {monsterName} 처치 완료!");
            Destroy(gameObject, 0.2f);
        }
    }
}
