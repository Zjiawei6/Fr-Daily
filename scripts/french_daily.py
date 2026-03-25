# French Daily Script

"This script will help track daily activities and reminders in French."

from datetime import datetime

if __name__ == '__main__':
    now = datetime.utcnow()
    print(f'Date et heure actuelles (UTC): {now.strftime("%Y-%m-%d %H:%M:%S")}')
    print('Rappels et activités du jour:')
    # Add your daily activities here
