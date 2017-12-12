

from datetime import datetime
from flask import render_template, \
    request, \
    session, \
    jsonify, \
    Blueprint
from app import app
from app.models import History
from app.database.utils import getEventsHistory
import logging

logger = logging.getLogger(app.config['LOG_FILE'])
history = Blueprint('history',
                   __name__,
                   template_folder='templates')


@history.route('/showHistory')
def showHistory():
    """
    Loading History page
    :return:
    """
    if session.get('user'):
        return render_template('history.html',
                               role=session.get('role'),
                               user=session.get('user'),
                               username=session.get('userName')
                               )

    else:
        logger.warning("User session was not found")
        return render_template('error.html', error='Unauthorized Access')

@history.route('/getHistoryEvents', methods=['POST'])
def getUserActionsHistory():
    """
    Get lock/unlock activity history of users
    :return:
    """
    try :
        startEventDate = datetime.strptime(request.values.get('date', None), '%Y-%m-%d')
        endEventDate = startEventDate.replace(minute=59, hour=23, second=59)
        if startEventDate:
            results = getEventsHistory(History, startEventDate, endEventDate)
            event = {}
            events = []
            for e in results:
                event["startTime"] = datetime.strftime(e.executed_on, '%H:%M')
                event["text"] = str(e.user_id).split("@")[0]+" "+e.action
                events.append(event.copy())
            return jsonify({'events':events})
        logger.warning("Can't parse startEventDate: %s ", startEventDate)
        return jsonify({'error':'Failed to get events'})
    except Exception as e :
        logger.warning(e)