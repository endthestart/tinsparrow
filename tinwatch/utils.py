import logging
import os
import re

from collections import defaultdict

log = logging.getLogger(__name__)


FILE_PATTERNS = [
    # "01 - Track 01" and "01": do nothing
    ur'^(\d+)\s*-\s*track\s*\d$',
    ur'^\d+$',

    # Useful patterns.
    ur'^(?P<artist>.+)-(?P<title>.+)-(?P<tag>.*)$',
    ur'^(?P<track>\d+)\s*-(?P<artist>.+)-(?P<title>.+)-(?P<tag>.*)$',
    ur'^(?P<track>\d+)\s(?P<artist>.+)-(?P<title>.+)-(?P<tag>.*)$',
    ur'^(?P<artist>.+)-(?P<title>.+)$',
    ur'^(?P<track>\d+)\.\s*(?P<artist>.+)-(?P<title>.+)$',
    ur'^(?P<track>\d+)\s*-\s*(?P<artist>.+)-(?P<title>.+)$',
    ur'^(?P<track>\d+)\s*-(?P<artist>.+)-(?P<title>.+)$',
    ur'^(?P<track>\d+)\s(?P<artist>.+)-(?P<title>.+)$',
    ur'^(?P<title>.+)$',
    ur'^(?P<track>\d+)\.\s*(?P<title>.+)$',
    ur'^(?P<track>\d+)\s*-\s*(?P<title>.+)$',
    ur'^(?P<track>\d+)\s(?P<title>.+)$',
    ur'^(?P<title>.+) by (?P<artist>.+)$',
]


def metadata_from_filename(file_path=None):
    if not file_path:
        log.warn("Must pass a full file path")
        return

    name, _ = os.path.splitext(os.path.basename(file_path))

    match = None
    for pattern in FILE_PATTERNS:
        m = re.match(pattern, name, re.IGNORECASE)
        if m and m.groupdict():
            match = m.groupdict()

    return match


def plurality(objs):
    """Given a sequence of comparable objects, returns the object that
    is most common in the set and the frequency of that object. The
    sequence must contain at least one object.
    """
    # Calculate frequencies.
    freqs = defaultdict(int)
    for obj in objs:
        freqs[obj] += 1

    if not freqs:
        raise ValueError('sequence must be non-empty')

    # Find object with maximum frequency.
    max_freq = 0
    res = None
    for obj, freq in freqs.items():
        if freq > max_freq:
            max_freq = freq
            res = obj

    return res, max_freq




