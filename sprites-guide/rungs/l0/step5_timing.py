"""Step 5 of the L0 rung page (section 2): predict, then time, a container pull and a container start.

Order matters here:

1. Fill in the two predictions below BEFORE you run anything with Docker.
2. Run `python3 run_timing.py`. It copies your predictions into timings.json at
   the moment it starts, so changing them afterwards does not count.
3. Write median() below.
4. Run `python3 check.py step5`.
"""

# TODO: your guesses, in seconds, before measuring anything.
# How long will `docker pull python:3.12` take on your connection, from nothing?
PREDICTED_PULL_SECONDS = None
# How long will `docker run --rm python:3.12 python -c 'print(1)'` take once the image is local?
PREDICTED_RUN_SECONDS = None

# TODO, only if the check tells you your ratio was off by more than 3x:
# one sentence on what you had wrong. That sentence is the point of the mission.
SURPRISE = ""


def median(xs):
    """Return the median of a non-empty list of numbers.

    Sort a copy (don't change the list you were given). With an odd count, the
    median is the middle value. With an even count, it is the average of the
    two middle values.
    """
    # TODO: your code here
    raise NotImplementedError("median")
