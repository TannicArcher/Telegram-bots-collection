from aiogram.dispatcher.filters.state import State, StatesGroup


class BroadcastState(StatesGroup):
    BS1 = State()
    BS2 = State()


class GiveBalState(StatesGroup):
    GB1 = State()
    GB2 = State()


class EditButtonState(StatesGroup):
    EC1 = State()
    EC2 = State()
    EC3 = State()
    EC4 = State()
    EC5 = State()


class SOSAdminStates(StatesGroup):
    SS1 = State()
    SS2 = State()


class AddCategory(StatesGroup):
    AC1 = State()


class AddSubCategory(StatesGroup):
    ASC1 = State()
    ASC2 = State()
    ASC3 = State()
    ASC4 = State()
    ASC5 = State()


class AddItem(StatesGroup):
    AI1 = State()
    AI2 = State()
    AI3 = State()
    AI4 = State()
    AI5 = State()
    AI6 = State()
    AI7 = State()


class DelCategory(StatesGroup):
    AC1 = State()


class DelSubCategory(StatesGroup):
    ASC1 = State()
    ASC2 = State()


class DelItem(StatesGroup):
    AI1 = State()
    AI2 = State()
    AI3 = State()


class GetUserState(StatesGroup):
    GU1 = State()
    GU2 = State()
    GU3 = State()


class EditChannelID(StatesGroup):
    EC1 = State()


class EditChannelURL(StatesGroup):
    EC1 = State()


class EditSecretKey(StatesGroup):
    EC1 = State()


class EditLogChannel(StatesGroup):
    EC1 = State()


class EditSettingsState(StatesGroup):
    E1 = State()
    E2 = State()


class EditCommission(StatesGroup):
    EC1 = State()


class EditPhone(StatesGroup):
    EC1 = State()


class AddPromoState(StatesGroup):
    P1 = State()

