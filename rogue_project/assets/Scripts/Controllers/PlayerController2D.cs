using UnityEngine;

namespace RogueProject2.Controllers
{
    /// <summary>
    /// Unity 2D Player Controller for Hero Duran (Paladin V6)
    /// </summary>
    [RequireComponent(typeof(Rigidbody2D))]
    public class PlayerController2D : MonoBehaviour
    {
        [Header("Movement Settings")]
        public float moveSpeed = 6.0f;
        public float dashSpeed = 12.0f;
        public float dashDuration = 0.2f;

        [Header("Player Stats")]
        public int currentHp = 100;
        public int maxHp = 100;
        public int currentMp = 50;
        public int maxMp = 50;
        public float currentSp = 0f;
        public float maxSp = 100f;
        public int level = 1;
        public int gold = 0;
        public int attackPower = 35;

        [Header("Components")]
        private Rigidbody2D rb;
        private Vector2 moveInput;
        private Vector2 lastFacingDir = Vector2.down;

        private bool isDashing = false;
        private float dashTimer = 0f;
        public bool isInvincible = false;
        private float invincibleTimer = 0f;

        private void Awake()
        {
            rb = GetComponent<Rigidbody2D>();
            rb.gravityScale = 0f;
            rb.freezeRotation = true;
        }

        private void Update()
        {
            HandleInput();
            HandleTimers();
        }

        private void FixedUpdate()
        {
            HandleMovement();
        }

        private void HandleInput()
        {
            float inputX = Input.GetAxisRaw("Horizontal");
            float inputY = Input.GetAxisRaw("Vertical");
            moveInput = new Vector2(inputX, inputY).normalized;

            if (moveInput != Vector2.zero)
            {
                lastFacingDir = moveInput;
            }

            // Dash / Dodge
            if (Input.GetKeyDown(KeyCode.LeftShift) && !isDashing)
            {
                StartDash();
            }
        }

        private void HandleMovement()
        {
            if (isDashing)
            {
                rb.velocity = lastFacingDir * dashSpeed;
            }
            else
            {
                rb.velocity = moveInput * moveSpeed;
            }
        }

        private void StartDash()
        {
            isDashing = true;
            isInvincible = true;
            dashTimer = dashDuration;
            invincibleTimer = dashDuration + 0.1f;
        }

        private void HandleTimers()
        {
            if (isDashing)
            {
                dashTimer -= Time.deltaTime;
                if (dashTimer <= 0f) isDashing = false;
            }

            if (isInvincible)
            {
                invincibleTimer -= Time.deltaTime;
                if (invincibleTimer <= 0f) isInvincible = false;
            }

            // MP Natural Regeneration
            if (currentMp < maxMp)
            {
                currentMp = Mathf.Min(maxMp, currentMp + Mathf.RoundToInt(5f * Time.deltaTime));
            }
        }

        public void TakeDamage(int damage)
        {
            if (isInvincible) return;

            currentHp = Mathf.Max(0, currentHp - damage);
            isInvincible = true;
            invincibleTimer = 1.0f; // 1 second invincibility

            if (currentHp <= 0)
            {
                OnDeath();
            }
        }

        public void AddSP(float amount)
        {
            currentSp = Mathf.Min(maxSp, currentSp + amount);
        }

        public Vector2 GetFacingDirection()
        {
            return lastFacingDir;
        }

        private void OnDeath()
        {
            Debug.Log("🛡️ 용사 슈드 (듀란 팔라딘) 사망 - Game Over");
            // Trigger UI Game Over
        }
    }
}
