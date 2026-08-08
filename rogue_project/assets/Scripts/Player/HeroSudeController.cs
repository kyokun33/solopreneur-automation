using UnityEngine;

namespace RogueProject2.Player
{
    /// <summary>
    /// Pure Unity 6 Hero Sude (슈드) Paladin V6 Controller
    /// 8-Direction RigidBody2D Physics Movement, Dash, 12 FPS Retro Timeline Frame Sync
    /// </summary>
    [RequireComponent(typeof(Rigidbody2D))]
    [RequireComponent(typeof(SpriteRenderer))]
    public class HeroSudeController : MonoBehaviour
    {
        [Header("Hero Profile")]
        public string heroName = "슈드 (Sude)";
        public string heroClass = "팔라딘 V6";
        public float moveSpeed = 6.0f;
        public float dashSpeed = 12.0f;

        [Header("Stats")]
        public int currentHp = 120;
        public int maxHp = 120;
        public int currentMp = 60;
        public int maxMp = 60;
        public float currentSp = 0f;
        public float maxSp = 100f;
        public int attackPower = 40;

        [Header("4-Direction Sprites")]
        public Sprite[] walkSouthSprites;
        public Sprite[] walkEastSprites;
        public Sprite[] walkWestSprites;
        public Sprite[] walkNorthSprites;

        private Rigidbody2D rb;
        private SpriteRenderer sr;
        private Vector2 moveInput;
        private Vector2 facingDir = Vector2.down;

        private int frameIndex = 0;
        private float animTimer = 0f;
        private const float FRAME_RATE = 12.0f; // 12 FPS Retro Animation

        public bool isInvincible = false;
        private float invincibleTimer = 0f;

        private void Awake()
        {
            rb = GetComponent<Rigidbody2D>();
            sr = GetComponent<SpriteRenderer>();
            rb.gravityScale = 0f;
            rb.freezeRotation = true;
        }

        private void Update()
        {
            HandleInput();
            HandleAnimationTimer();
            HandleTimers();
        }

        private void FixedUpdate()
        {
            rb.velocity = moveInput * moveSpeed;
        }

        private void HandleInput()
        {
            float x = Input.GetAxisRaw("Horizontal");
            float y = Input.GetAxisRaw("Vertical");
            moveInput = new Vector2(x, y).normalized;

            if (moveInput != Vector2.zero)
            {
                facingDir = moveInput;
            }

            if (Input.GetKeyDown(KeyCode.LeftShift) && !isInvincible)
            {
                isInvincible = true;
                invincibleTimer = 0.3f;
            }
        }

        private void HandleAnimationTimer()
        {
            if (moveInput != Vector2.zero)
            {
                animTimer += Time.deltaTime;
                if (animTimer >= (1.0f / FRAME_RATE))
                {
                    animTimer = 0f;
                    frameIndex = (frameIndex + 1) % 4;
                    UpdateSprite();
                }
            }
            else
            {
                frameIndex = 0;
                UpdateSprite();
            }
        }

        private void UpdateSprite()
        {
            if (Mathf.Abs(facingDir.x) > Mathf.Abs(facingDir.y))
            {
                if (facingDir.x > 0 && walkEastSprites != null && walkEastSprites.Length > 0)
                    sr.sprite = walkEastSprites[frameIndex % walkEastSprites.Length];
                else if (facingDir.x < 0 && walkWestSprites != null && walkWestSprites.Length > 0)
                    sr.sprite = walkWestSprites[frameIndex % walkWestSprites.Length];
            }
            else
            {
                if (facingDir.y > 0 && walkNorthSprites != null && walkNorthSprites.Length > 0)
                    sr.sprite = walkNorthSprites[frameIndex % walkNorthSprites.Length];
                else if (facingDir.y <= 0 && walkSouthSprites != null && walkSouthSprites.Length > 0)
                    sr.sprite = walkSouthSprites[frameIndex % walkSouthSprites.Length];
            }
        }

        private void HandleTimers()
        {
            if (isInvincible)
            {
                invincibleTimer -= Time.deltaTime;
                sr.color = (Mathf.FloorToInt(Time.time * 20) % 2 == 0) ? new Color(1, 1, 1, 0.4f) : Color.white;
                if (invincibleTimer <= 0f)
                {
                    isInvincible = false;
                    sr.color = Color.white;
                }
            }

            if (currentMp < maxMp)
            {
                currentMp = Mathf.Min(maxMp, currentMp + Mathf.RoundToInt(4f * Time.deltaTime));
            }
        }

        public void TakeDamage(int damage)
        {
            if (isInvincible) return;

            currentHp = Mathf.Max(0, currentHp - damage);
            isInvincible = true;
            invincibleTimer = 1.0f;

            if (currentHp <= 0)
            {
                Debug.Log("🛡️ 용사 슈드 (Sude) 전사");
            }
        }

        public void AddSP(float amount)
        {
            currentSp = Mathf.Min(maxSp, currentSp + amount);
        }

        public Vector2 GetFacingDirection()
        {
            return facingDir;
        }
    }
}
