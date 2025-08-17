import subprocess


def test_ffmpeg_installed() -> None:
    """Verify that ffmpeg is installed and accessible on the PATH."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        raise AssertionError("ffmpeg is not installed or not in PATH")
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"ffmpeg exists but failed to run: {e}")

    # Quick sanity check: output should mention "ffmpeg"
    assert "ffmpeg" in result.stdout.lower()
