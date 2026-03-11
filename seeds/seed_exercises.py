"""
Run this script once to populate the exercises table with starter data.
Usage: python seeds/seed_exercises.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.exercise import Exercise

EXERCISES = [
    {
        "name": "Push Ups",
        "muscle_groups": "Chest, Triceps, Shoulders",
        "description": "A foundational upper-body compound movement using only your bodyweight. Builds chest, shoulder, and arm strength simultaneously.",
        "instructions": "1. Place hands shoulder-width apart on the floor.\n2. Keep your body in a straight line from head to heels.\n3. Lower your chest to 1 inch above the floor.\n4. Push back up explosively.\n5. Keep your core tight throughout the movement.",
        "common_mistakes": "Sagging hips, flared elbows past 90 degrees, incomplete range of motion, holding your breath.",
        "difficulty": "Beginner", "base_sets": 3, "base_reps": 8, "rest_seconds": 60,
        "workout_type": "Upper Body", "image_url": None,
    },
    {
        "name": "Squats",
        "muscle_groups": "Quads, Glutes, Hamstrings",
        "description": "The king of lower-body exercises. Trains the entire lower body with emphasis on quads and glutes.",
        "instructions": "1. Stand feet shoulder-width apart, toes slightly out.\n2. Sit back and down as if onto a chair.\n3. Keep chest up and knees tracking over toes.\n4. Descend until thighs are parallel to the floor.\n5. Drive through heels to return to standing.",
        "common_mistakes": "Knees caving inward, heels lifting off the floor, torso collapsing forward, not reaching depth.",
        "difficulty": "Beginner", "base_sets": 3, "base_reps": 12, "rest_seconds": 60,
        "workout_type": "Lower Body", "image_url": None,
    },
    {
        "name": "Plank",
        "muscle_groups": "Core, Shoulders, Glutes",
        "description": "An isometric core stabilisation exercise that trains the deep core muscles responsible for posture and spinal support.",
        "instructions": "1. Place forearms flat on the floor, elbows under shoulders.\n2. Keep your body in a straight line from head to heels.\n3. Squeeze your core and glutes.\n4. Breathe steadily and hold the position.",
        "common_mistakes": "Raised hips, sagging lower back, head drooping, holding your breath.",
        "difficulty": "Beginner", "base_sets": 3, "base_reps": 20, "rest_seconds": 45,
        "workout_type": "Core", "image_url": None,
    },
    {
        "name": "Lunges",
        "muscle_groups": "Quads, Glutes, Hamstrings",
        "description": "A unilateral leg exercise that improves balance, coordination, and lower body strength.",
        "instructions": "1. Stand upright with feet together.\n2. Step one foot forward.\n3. Lower your back knee to 1 inch from the floor.\n4. Push back through your front heel to return.\n5. Alternate legs each rep.",
        "common_mistakes": "Front knee shooting past toes, torso leaning too far forward, not keeping core tight.",
        "difficulty": "Beginner", "base_sets": 3, "base_reps": 10, "rest_seconds": 60,
        "workout_type": "Lower Body", "image_url": None,
    },
    {
        "name": "Glute Bridge",
        "muscle_groups": "Glutes, Hamstrings, Core",
        "description": "A hip extension exercise targeting the posterior chain, particularly the glutes and hamstrings.",
        "instructions": "1. Lie on your back with feet flat on the floor.\n2. Push your hips toward the ceiling by squeezing your glutes.\n3. Hold at the top for 1-2 seconds.\n4. Lower slowly back down.",
        "common_mistakes": "Arching the lower back, not squeezing glutes at the top, feet too far from body.",
        "difficulty": "Beginner", "base_sets": 3, "base_reps": 15, "rest_seconds": 45,
        "workout_type": "Lower Body", "image_url": None,
    },
    {
        "name": "Wall Sit",
        "muscle_groups": "Quads, Glutes",
        "description": "An isometric quad exercise that mimics the seated position and builds endurance in the lower body.",
        "instructions": "1. Stand with your back flat against a wall.\n2. Slide down until thighs are parallel to the floor.\n3. Keep knees directly above ankles.\n4. Hold the position for the prescribed time.",
        "common_mistakes": "Thighs above parallel, placing hands on knees for support, feet too close to wall.",
        "difficulty": "Beginner", "base_sets": 3, "base_reps": 30, "rest_seconds": 60,
        "workout_type": "Lower Body", "image_url": None,
    },
    {
        "name": "Tricep Dips",
        "muscle_groups": "Triceps, Chest, Shoulders",
        "description": "An upper-body push exercise using a chair or parallel bars that heavily targets the triceps.",
        "instructions": "1. Place your hands on the edge of a sturdy chair behind you.\n2. Extend legs out in front.\n3. Lower your body by bending elbows to 90 degrees.\n4. Push back up until arms are straight.",
        "common_mistakes": "Elbows flaring outward, not reaching full depth, shrugging the shoulders.",
        "difficulty": "Beginner", "base_sets": 3, "base_reps": 10, "rest_seconds": 60,
        "workout_type": "Upper Body", "image_url": None,
    },
    {
        "name": "Superman Hold",
        "muscle_groups": "Lower Back, Glutes",
        "description": "A back extension exercise that strengthens the posterior chain and improves spinal stability.",
        "instructions": "1. Lie face down with arms extended in front.\n2. Simultaneously lift your arms, chest, and legs off the floor.\n3. Hold briefly at the top.\n4. Lower slowly and repeat.",
        "common_mistakes": "Jerking into the position, craning the neck upward, not fully extending.",
        "difficulty": "Beginner", "base_sets": 3, "base_reps": 10, "rest_seconds": 45,
        "workout_type": "Core", "image_url": None,
    },
    {
        "name": "Mountain Climbers",
        "muscle_groups": "Core, Shoulders, Cardio",
        "description": "A dynamic full-body movement combining core strengthening and cardiovascular conditioning.",
        "instructions": "1. Start in a high plank position.\n2. Drive one knee to your chest.\n3. Quickly switch legs in a running motion.\n4. Keep hips level throughout the movement.",
        "common_mistakes": "Bouncing hips up and down, slowing down too much, sagging back.",
        "difficulty": "Intermediate", "base_sets": 3, "base_reps": 20, "rest_seconds": 60,
        "workout_type": "Full Body", "image_url": None,
    },
    {
        "name": "Bicycle Crunch",
        "muscle_groups": "Core, Obliques",
        "description": "A rotational core movement that targets the obliques and rectus abdominis simultaneously.",
        "instructions": "1. Lie on your back with hands behind your head.\n2. Bring your right elbow toward your left knee.\n3. Simultaneously extend your right leg.\n4. Switch sides in a controlled cycling motion.",
        "common_mistakes": "Pulling the neck forward, rushing through the motion, not fully rotating.",
        "difficulty": "Intermediate", "base_sets": 3, "base_reps": 16, "rest_seconds": 45,
        "workout_type": "Core", "image_url": None,
    },
    {
        "name": "Jump Squats",
        "muscle_groups": "Quads, Glutes, Cardio",
        "description": "An explosive plyometric squat variation that develops lower body power and cardiovascular fitness.",
        "instructions": "1. Perform a regular squat.\n2. As you come up, explode upward into a jump.\n3. Land softly with bent knees to absorb impact.\n4. Go straight into the next rep.",
        "common_mistakes": "Landing with locked knees, not absorbing the impact, shallow squat depth.",
        "difficulty": "Intermediate", "base_sets": 3, "base_reps": 10, "rest_seconds": 75,
        "workout_type": "Lower Body", "image_url": None,
    },
    {
        "name": "Pike Push Ups",
        "muscle_groups": "Shoulders, Triceps",
        "description": "An inverted push-up variation that targets the deltoids far more than standard push-ups.",
        "instructions": "1. Start in a downward dog position with hips high.\n2. Bend elbows to lower the top of your head toward the floor.\n3. Push back up to the starting position.\n4. Keep hips elevated throughout.",
        "common_mistakes": "Not keeping hips elevated, half range of motion, feet too close to hands.",
        "difficulty": "Intermediate", "base_sets": 3, "base_reps": 8, "rest_seconds": 60,
        "workout_type": "Upper Body", "image_url": None,
    },
    {
        "name": "Leg Raises",
        "muscle_groups": "Core, Hip Flexors",
        "description": "A lower abdominal isolation exercise that challenges the core and hip flexors.",
        "instructions": "1. Lie flat on your back, legs straight.\n2. Place hands under your glutes for support.\n3. Raise legs to 90 degrees keeping them straight.\n4. Lower slowly without letting them touch the floor.",
        "common_mistakes": "Arching the lower back off the floor, using momentum, bending the knees.",
        "difficulty": "Intermediate", "base_sets": 3, "base_reps": 10, "rest_seconds": 45,
        "workout_type": "Core", "image_url": None,
    },
    {
        "name": "Pull Ups",
        "muscle_groups": "Back, Biceps, Core",
        "description": "The gold standard upper-body pulling exercise. Builds a wide, strong back and thick biceps using only a pull-up bar.",
        "instructions": "1. Hang from a bar with arms fully extended, overhand grip.\n2. Engage your shoulder blades and pull elbows toward your hips.\n3. Pull until your chin clears the bar.\n4. Lower slowly with full control.",
        "common_mistakes": "Using kipping momentum, not reaching full arm extension at the bottom, crossing ankles.",
        "difficulty": "Advanced", "base_sets": 3, "base_reps": 5, "rest_seconds": 90,
        "workout_type": "Upper Body", "image_url": None,
    },
    {
        "name": "Burpees",
        "muscle_groups": "Full Body, Cardio",
        "description": "A total-body explosive conditioning movement that combines strength and cardiovascular training.",
        "instructions": "1. Stand upright.\n2. Squat down and place hands on the floor.\n3. Jump feet back to a plank position.\n4. Perform a push-up.\n5. Jump feet back to squat.\n6. Explode upward into a jump with arms overhead.",
        "common_mistakes": "Skipping the push-up, no jump at the top, sloppy plank position.",
        "difficulty": "Advanced", "base_sets": 3, "base_reps": 8, "rest_seconds": 90,
        "workout_type": "Full Body", "image_url": None,
    },
]

def seed():
    db = SessionLocal()
    try:
        existing = db.query(Exercise).count()
        if existing > 0:
            print(f"Already seeded ({existing} exercises). Skipping.")
            return
        for data in EXERCISES:
            db.add(Exercise(**data))
        db.commit()
        print(f"✅ Seeded {len(EXERCISES)} exercises successfully.")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
