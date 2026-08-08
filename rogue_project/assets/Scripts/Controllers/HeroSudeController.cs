using UnityEngine;

namespace RogueProject2.Controllers
{
    /// <summary>
    /// Unity 2D Hero Sude (슈드) Dedicated Controller
    /// Classes: Paladin V6
    /// Skills: Holy Slash (Q), Holy Shield (W), Consecration (E), Angel Blade (R), Divine Intervention (Space)
    /// </summary>
    [RequireComponent(typeof(Rigidbody2D))]
    [RequireComponent(typeof(SpriteRenderer))]
    [RequireComponent(typeof(Animator))]
    public class HeroSudeController : MonoBehaviour
    {
        [Header("Hero Sude Profile")]
        public string heroName = "슈드 (Sude)";
        public string heroClass = "팔라딘 V6 (Paladin V6)";
        public float moveSpeed = 6.0f;

        [Header("Stats")]
        public int currentHp = 120;
        public int maxHp = 120;
        public int currentMp = 60;
        public int maxMp = 60;
        public float currentSp = 0f;
        public float maxSp = 100f;
        public int level = 1;
        public int attackPower = 40;

        [Header("4-Direction Animations (South, East, West, North)")]
        public Sprite[] walkSouthSprites;
        public Sprite[] walkEastSprites;
        public Sprite[] walkWestSprites;
        public Sprite[] walkNorthSprites;
        public Sprite[] attackSprites;
        public Sprite[] ultimateSprites;

        [Header("Runtime State")]
        private Rigidbody2D rb;
        private SpriteRenderer spriteRenderer;
        private Vector2 moveInput;
        private Vector2 facingDirection = Vector2.down;
        private int animFrameIndex = 0;
        private float animTimer = 0f;
        public float frameRate = 12f; // Authentic 12 FPS Retro Sprite Animation

        public bool isInvincible = false;
        private float invincibleTimer = 0f;

        private void Awake()
        {
            rb = GetComponent<Rigidbody2D>();
            spriteRenderer = GetComponent<SpriteRenderer>();
            rb.gravityScale = 0f;
            rb.freezeRotation = true;
        }

        private void Update()
        {
            HandleInput();
            HandleAnimationTimer();
            HandleInvincibility();
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
                facingDirection = moveInput;
            }

            // Skills
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

        private void HandleAnimationTimer()
        {
            if (moveInput != Vector2.zero)
            {
                animTimer += Time.deltaTime;
                if (animTimer >= (1f / frameRate))
                {
                    animTimer = 0f;
                    animFrameIndex = (animFrameIndex + 1) % 4;
                    UpdateSpriteFrame();
                }
            }
            else
            {
                animFrameIndex = 0;
                UpdateSpriteFrame();
            }
        }

        private void UpdateSpriteFrame()
        {
            // 4-Direction Sprite Frame Selector for Hero Sude
            if (Mathf.Abs(facingDirection.x) > Mathf.Abs(facingDirection.y))
            {
                if (facingDirection.x > 0)
                {
                    if (walkEastSprites != null && walkEastSprites.Length > 0)
                        spriteRenderer.sprite = walkEastSprites[animFrameIndex % walkEastSprites.Length];
                }
                else
                {
                    if (walkWestSprites != null && walkWestSprites.Length > 0)
                        spriteRenderer.sprite = walkWestSprites[animFrameIndex % walkWestSprites.Length];
                }
            }
            else
            {
                if (facingDirection.y > 0)
                {
                    if (walkNorthSprites != null && walkNorthSprites.Length > 0)
                        spriteRenderer.sprite = walkNorthSprites[animFrameIndex % walkNorthSprites.Length];
                }
                else
                {
                    if (walkSouthSprites != null && walkSouthSprites.Length > 0)
                        spriteRenderer.sprite = walkSouthSprites[animFrameIndex % walkSouthSprites.Length];
                }
            }
        }

        private void HandleInvincibility()
        {
            if (isInvincible)
            {
                invincibleTimer -= Time.deltaTime;
                spriteRenderer.color = (Mathf.FloorToInt(Time.time * 20) % 2 == 0) ? new Color(1, 1, 1, 0.4f) : Color.white;
                if (invincibleTimer <= 0f)
                {
                    isInvincible = false;
                    spriteRenderer.color = Color.white;
                }
            }
        }

        public void CastHolySlash()
        {
            Debug.Log($"⚔️ [용사 슈드] 성스러운 베기 (Holy Slash) 시전!");
            AddSP(10f);
        }

        public void CastHolyShield()
        {
            if (currentMp >= 15)
            {
                currentMp -= 15;
                isInvincible = true;
                invincibleTimer = 3.0f;
                Debug.Log($"🛡️ [용사 슈드] 신성한 방패 (Holy Shield) 3초 전개!");
            }
        }

        public void CastConsecration()
        {
            if (currentMp >= 20)
            {
                currentMp -= 20;
                Debug.Log($"✨ [용사 슈드] 축성 (Consecration) 마법진 생성!");
            }
        }

        public void CastAngelBlade()
        {
            if (currentMp >= 25)
            {
                currentMp -= 25;
                Debug.Log($"👼 [용사 슈드] 천사의 검 (Angel Blade) 발사!");
            }
        }

        public void AddSP(float val)
        {
            currentSp = Mathf.Min(maxSp, currentSp + val);
        }
    }
}
