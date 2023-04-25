import re

stringa = "Voglio avere informazioni su cpu, ram e batteria"
pattern = r"(?=.*\bcpu\b|\bram\b|\bbatteria\b)(?P<cpu>\bcpu\b)?(?P<ram>\bram\b)?(?P<batteria>\bbatteria\b)?"

match = re.search(pattern, stringa)

if match:
    print(match.groupdict())