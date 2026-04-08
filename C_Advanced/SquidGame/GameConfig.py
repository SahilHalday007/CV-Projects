# GameConfig.py - Configuration and difficulty settings

class GameDifficulty:
    """Define difficulty presets"""

    EASY = {
        'name': 'Easy',
        'threshold_difficulty': 30,
        'time_total': 60,
        'width_start_ratio': 0.30,
        'width_end_ratio': 0.65,
        'green_light_duration': 3,
        'red_light_min': 40,
        'red_light_max': 70
    }

    MEDIUM = {
        'name': 'Medium',
        'threshold_difficulty': 20,
        'time_total': 45,
        'width_start_ratio': 0.35,
        'width_end_ratio': 0.55,
        'green_light_duration': 2,
        'red_light_min': 30,
        'red_light_max': 50
    }

    HARD = {
        'name': 'Hard',
        'threshold_difficulty': 10,
        'time_total': 30,
        'width_start_ratio': 0.40,
        'width_end_ratio': 0.50,
        'green_light_duration': 1.5,
        'red_light_min': 20,
        'red_light_max': 35
    }

    EXTREME = {
        'name': 'Extreme',
        'threshold_difficulty': 5,
        'time_total': 20,
        'width_start_ratio': 0.45,
        'width_end_ratio': 0.48,
        'green_light_duration': 1,
        'red_light_min': 15,
        'red_light_max': 25
    }


class GameStatistics:
    """Track player statistics"""

    def __init__(self):
        self.games_played = 0
        self.games_won = 0
        self.games_lost = 0
        self.total_time_played = 0
        self.eliminations = 0
        self.avg_survival_time = 0

    def record_win(self, time_survived):
        """Record a win"""
        self.games_played += 1
        self.games_won += 1
        self.total_time_played += time_survived
        self.avg_survival_time = self.total_time_played / self.games_played

    def record_loss(self, time_survived):
        """Record a loss"""
        self.games_played += 1
        self.games_lost += 1
        self.eliminations += 1
        self.total_time_played += time_survived
        self.avg_survival_time = self.total_time_played / self.games_played

    def get_win_rate(self):
        """Calculate win rate percentage"""
        if self.games_played == 0:
            return 0
        return (self.games_won / self.games_played) * 100

    def get_stats_dict(self):
        """Return stats as dictionary"""
        return {
            'games_played': self.games_played,
            'games_won': self.games_won,
            'games_lost': self.games_lost,
            'win_rate': self.get_win_rate(),
            'total_time_played': self.total_time_played,
            'avg_survival_time': self.avg_survival_time,
            'eliminations': self.eliminations
        }

    def print_stats(self):
        """Print formatted statistics"""
        print("\n=== GAME STATISTICS ===")
        print(f"Games Played: {self.games_played}")
        print(f"Games Won: {self.games_won}")
        print(f"Games Lost: {self.games_lost}")
        print(f"Win Rate: {self.get_win_rate():.1f}%")
        print(f"Total Time: {self.total_time_played:.1f}s")
        print(f"Avg Survival: {self.avg_survival_time:.1f}s")
        print(f"Eliminations: {self.eliminations}")
        print("=======================\n")


class GameAudio:
    """Manage game audio"""

    def __init__(self):
        self.sounds = {}
        self.volume = 0.7
        self.music_enabled = True
        self.sfx_enabled = True

    def load_sound(self, name, path):
        """Load a sound file"""
        try:
            import pygame
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.volume)
            self.sounds[name] = sound
        except Exception as e:
            print(f"Error loading sound {name}: {e}")

    def play_sound(self, name):
        """Play a sound"""
        if self.sfx_enabled and name in self.sounds:
            self.sounds[name].play()

    def set_volume(self, volume):
        """Set master volume (0-1)"""
        self.volume = max(0, min(1, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)

    def toggle_sfx(self):
        """Toggle sound effects"""
        self.sfx_enabled = not self.sfx_enabled
        return self.sfx_enabled


class PerformanceMonitor:
    """Monitor game performance"""

    def __init__(self):
        self.frame_times = []
        self.fps_history = []
        self.max_samples = 100

    def record_frame_time(self, frame_time):
        """Record frame time"""
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)

    def get_avg_fps(self):
        """Get average FPS"""
        if not self.frame_times or sum(self.frame_times) == 0:
            return 0
        avg_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_time if avg_time > 0 else 0

    def get_min_fps(self):
        """Get minimum FPS"""
        if not self.frame_times:
            return 0
        min_time = max(self.frame_times)
        return 1.0 / min_time if min_time > 0 else 0

    def get_max_fps(self):
        """Get maximum FPS"""
        if not self.frame_times:
            return 0
        max_time = min(self.frame_times)
        return 1.0 / max_time if max_time > 0 else 0

    def print_performance(self):
        """Print performance metrics"""
        print("\n=== PERFORMANCE ===")
        print(f"Avg FPS: {self.get_avg_fps():.1f}")
        print(f"Min FPS: {self.get_min_fps():.1f}")
        print(f"Max FPS: {self.get_max_fps():.1f}")
        print("===================\n")


# Example usage and integration

def initialize_game_with_difficulty(difficulty_name):
    """Initialize game with specified difficulty"""

    difficulty_map = {
        'easy': GameDifficulty.EASY,
        'medium': GameDifficulty.MEDIUM,
        'hard': GameDifficulty.HARD,
        'extreme': GameDifficulty.EXTREME
    }

    if difficulty_name.lower() not in difficulty_map:
        print(f"Unknown difficulty: {difficulty_name}")
        return GameDifficulty.MEDIUM

    return difficulty_map[difficulty_name.lower()]


def create_game_systems():
    """Create all game systems"""
    stats = GameStatistics()
    audio = GameAudio()
    perf_monitor = PerformanceMonitor()

    return {
        'stats': stats,
        'audio': audio,
        'performance': perf_monitor
    }


# Save and load statistics

def save_statistics(stats, filename="game_stats.json"):
    """Save statistics to file"""
    import json
    try:
        with open(filename, 'w') as f:
            json.dump(stats.get_stats_dict(), f, indent=2)
        print(f"Statistics saved to {filename}")
    except Exception as e:
        print(f"Error saving statistics: {e}")


def load_statistics(filename="game_stats.json"):
    """Load statistics from file"""
    import json
    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        stats = GameStatistics()
        stats.games_played = data.get('games_played', 0)
        stats.games_won = data.get('games_won', 0)
        stats.games_lost = data.get('games_lost', 0)
        stats.total_time_played = data.get('total_time_played', 0)
        stats.eliminations = data.get('eliminations', 0)

        if stats.games_played > 0:
            stats.avg_survival_time = stats.total_time_played / stats.games_played

        print(f"Statistics loaded from {filename}")
        return stats
    except FileNotFoundError:
        print(f"No statistics file found: {filename}")
        return GameStatistics()
    except Exception as e:
        print(f"Error loading statistics: {e}")
        return GameStatistics()