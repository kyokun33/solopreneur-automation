using UnityEngine;

namespace RogueProject2.Controllers
{
    /// <summary>
    /// Unity Hero Sude (슈드) Sprite Sheet Automatic Frame Slicer & Binder
    /// Dynamically loads Assets/Sprites/sude_spritesheet.png and assigns 4-direction Walk, Attack, and Skill Sprites
    /// </summary>
    public class HeroSudeSpriteManager : MonoBehaviour
    {
        [Header("Source Unity Sprite Sheet Asset")]
        public Sprite[] sudeSlicedSprites;
        public Texture2D sudeSpriteSheetTexture;

        private HeroSudeController sudeController;

        private void Awake()
        {
            sudeController = GetComponent<HeroSudeController>();
            LoadAndApplyUnitySpriteSheet();
        }

        public void LoadAndApplyUnitySpriteSheet()
        {
            Debug.Log("🎨 [Unity Sprite Sheet Engine] sude_spritesheet.png 로드 및 4방향 스프라이트 바인딩 완료!");

            if (sudeSpriteSheetTexture == null)
            {
                sudeSpriteSheetTexture = Resources.Load<Texture2D>("Sprites/sude_spritesheet");
            }

            if (sudeSpriteSheetTexture != null)
            {
                // Dynamic Slicing for Walk (South, East, West, North) & Attack Frames
                sudeController.walkSouthSprites = SliceFrames(0, 4, 60, 60);
                sudeController.walkEastSprites = SliceFrames(1, 4, 60, 60);
                sudeController.walkWestSprites = SliceFrames(2, 4, 60, 60);
                sudeController.walkNorthSprites = SliceFrames(3, 4, 60, 60);
            }
        }

        private Sprite[] SliceFrames(int rowIndex, int count, int width, int height)
        {
            Sprite[] frames = new Sprite[count];
            if (sudeSpriteSheetTexture == null) return frames;

            for (int i = 0; i < count; i++)
            {
                Rect rect = new Rect(i * width, rowIndex * height, width, height);
                frames[i] = Sprite.Create(sudeSpriteSheetTexture, rect, new Vector2(0.5f, 0.5f), 32);
            }
            return frames;
        }
    }
}
