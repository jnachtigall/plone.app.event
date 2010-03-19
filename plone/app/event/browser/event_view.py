from Products.Five.browser import BrowserView
from Products.CMFPlone.i18nl10n import ulocalized_time
from plone.app.event import event_util

from Products.DateRecurringIndex.recurring import RRuleICal
from Products.DateRecurringIndex.interfaces import IRecurringSequence

class EventView(BrowserView):

    def date_for_display(self):
        return event_util.toDisplay(self.context)

    def get_occurences(self):
        from Products.CMFCore.utils import getToolByName
        cat = getToolByName(self, 'portal_catalog')

        delta = [eval(rr) for rr in getattr(self.context, 'recurrence', None) if isinstance(rr,str) or rr]
        starts = IRecurringSequence(RRuleICal(self.context.start(), delta))
        ends = IRecurringSequence(RRuleICal(self.context.end(), delta))

        events = map(
            lambda start,end:dict(
                start_date = ulocalized_time(start, False, time_only=None, context=self.context),
                end_date = ulocalized_time(end, False, time_only=None, context=self.context),
                start_time = ulocalized_time(start, False, time_only=True, context=self.context),
                end_time = ulocalized_time(end, False, time_only=True, context=self.context),
                same_day = event_util.isSameDay(self.context),
                same_time = event_util.isSameTime(self.context),
            ), starts, ends )

        """
        # TODO: don't ask the index for occurences, calculate them from recrule
        # index is integer representation which cannot (really?) be reversed
        # see Products.DateRecurringIndex.utils.dt2int
        events = None
        cat_item = cat.searchResults(**{'UID':self.context.UID()})
        if cat_item:
            events = map(
                lambda start,end:dict(
                    start_date = ulocalized_time(start, False, time_only=None, context=self.context),
                    end_date = ulocalized_time(end, False, time_only=None, context=self.context),
                    start_time = ulocalized_time(start, False, time_only=True, context=self.context),
                    end_time = ulocalized_time(end, False, time_only=True, context=self.context),
                    same_day = event_util.isSameDay(self.context),
                    same_time = event_util.isSameTime(self.context),
                ),
                cat.getIndexDataForRID(cat_item[0].getRID())['start'],
                cat.getIndexDataForRID(cat_item[0].getRID())['end']
                )
        """
        return events
