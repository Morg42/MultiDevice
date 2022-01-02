#!/usr/bin/env python3
# test.py

_VERSION     = '0.1.0'
_DESCRIPTION = 'Dependencies for multidevice plugin'

import logging
import re
_logger = logging.getLogger(__name__)

def checkdepencies(sh, dependencies):
    '''
    check if dependencies are fullfilled. This userfunction could be implemented in an eval function as such:
    eval: value if uf.multidevice.checkdepencies(sh, sh..dependencies) else None
    This means, the item can only be updated (via Admin IF, CLI, Visu, etc.) if dependencies are fullfilled.
    The respective list is stored in an item, usually a child of the relevant command item called "dependencies".
    It contains strings with the syntax '<item path> (relative or absolute)<operator> (==, >=, >, <=, <, !=) <value>'.

    The main entries in the list are evaluated as AND, whereas entries within sub-lists are treated as OR.

    Examples:
    Example 1: is true if ALL given comparisons are true:
    ['...power == True', '...mute == True', '...volume >= 100']
    Example 2: is true if ANY given comparison is true. Evaluation stops on first true comparison:
    [['...power == True', '...mute == True', '...volume != 100']]
    Example 3: is true if power is true AND (mute is true OR volume is higher than 100)
    ['...power == True', ['...mute == True', '...volume > 100']]

    :param sh: smarthome object
    :type sh: object
    :param dependencies: (relative) item containing list of dependencies, usually sh..dependencies
    :type sh: SHNG item
    '''
    def test_singleentry(parent, data):
        '''
        check every single entry in the dependency list(s) if the comparisons are true or not

        :param parent: smarthome item defined as the base for detecting relative items
        :type parent: SHNG item
        :param data: one single entry of the dependency list(s)
        :type data: str
        '''
        # If data is no str, ignore
        if not isinstance(data, str):
            _logger.warning(f'Testing dependency: {data} is no string, can not evaluate')
            return 1
        # Split string into item, operator, value
        res = [x.strip() for x in re.split('(==|<=|>=|>|<|!=|is)', data)]
        # If format "item operator value" is not fullfilled, ignore
        if not len(res) == 3:
            _logger.warning(f'Testing dependency: {res} has wrong format, ignoring.')
            return 1
        # comparison operator
        compare = res[1]
        # get SHNG item from relative item declaration
        item = sh.return_item(parent.get_absolutepath(res[0]))
        if item is None:
            _logger.warning(f'Testing dependency: Item {fullpath} does not exist, ignoring.')
            return 1

        # convert string to bool or num if item type corresponds
        if item.property.type == "bool":
            if res[2].lower() in ["true", "yes"]:
                comparevalue = True
            elif res[2].lower() in ["false", "no"]:
                comparevalue = False
            else:
                comparevalue = None
        if item.property.type == "num":
            comparevalue = float(res[2])

        # look up comparisons based on operator
        singleresult = op[compare](item(), comparevalue)
        _logger.debug(f'Testing dependency: {item} {compare} {comparevalue} results in {singleresult}')
        return int(singleresult)

    # read item value
    list_content = dependencies()
    totalcount = len(list_content)
    _logger.info(f'Testing dependency: {list_content} (total {totalcount})')
    # convert string operators to real comparison operator
    op = {'==': lambda x, y: x == y,
          '>=': lambda x, y: x >= y,
          '>': lambda x, y: x > y,
          '<=': lambda x, y: x <= y,
          '<': lambda x, y: x < y,
          '!=': lambda x, y: not x == y,
          'is': lambda x, y: x == y}
    # iterate through main list
    for data in list_content:
        # check if entry is sub-dict (containing OR declarations)
        if isinstance(data, list):
            # iterate through sub-list
            for groupentry in data:
                # break iteration and count hits correctly as soon as one comparison is true
                if test_singleentry(dependencies, groupentry):
                    totalcount -= 1
                    _logger.debug(f'Testing dependency: At least one entry in sub-list {data} is True. Continuing with main list.')
                    break
        else:
            # subtract 1 from total count if comparison result is true.
            totalcount -= test_singleentry(dependencies, data)
    if totalcount == 0:
        _logger.info(f'Testing dependency: all dependencies fullfilled, return True.')
        return True
    else:
        _logger.info(f'Testing dependency: dependencies NOT fullfilled, return False.')
        return False
