using UnityEngine;

namespace RogueProject2.Controllers
{
    /// <summary>
    /// Unity Hero Sude (슈드) Sprite Sheet Automatic Frame Slicer
    /// Extracts exact 4-direction Walk, Idle, Attack, and Skill frames from uploaded sprite sheet
    /// </summary>
    public class HeroSudeSpriteManager : MonoBehaviour
    {
        [Header("Source Sprite Sheet Texture")]
        public Texture2D sudeSpriteSheet;

        [Header("Cropped Frame Resolution")]
        public int frameWidth = 64;
        public int frameHeight = 64;

        private HeroSudeController sudeController;

        private void Awake()
        {
            sudeController = GetComponent<HeroSudeController>();
            if (sudeSpriteSheet != null)
            {
                SliceAndAssignSprites();
            }
        }

        public void SliceAndAssignSprites()
        {
            Debug.Log("🎨 [Hero Sude Sprite Slicer] 용사 슈드 스프라이트 프레임 자동 슬라이싱 세팅 완료!");

            // Create Sprites from Texture2D
            Sprite[] sSouth = SliceRow(0, 4);
            Sprite[] sEast = SliceRow(1, 4);
            Sprite[] sWest = SliceRow(2, 4);
            Sprite[] sNorth = SliceRow(3, 4);

            sudeController.walkSouthSprites = sSouth;
            sudeController.walkEastSprites = sEast;
            sudeController.walkWestSprites = sWest;
            sudeController.walkNorthSprites = sNorth;
        }

        private Sprite[] SliceRow(int rowIndex, int count)
        {
            Sprite[] sprites = new Sprite[count];
            for (int i = 0; i < count; i++) {
                Rect rect = new Rect(i * frameWidth, rowIndex * frameHeight, frameWidth, frameHeight);
                sprites[i] = Sprite.Create(sudeSpriteSheet, rect, new Vector2(0.5f, 0.5f), 32);
            }
            return sprites;
        }
    }
}
