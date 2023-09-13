from aiogram.dispatcher.filters.state import StatesGroup, State


class BalanceState(StatesGroup):
    BS1 = State()
    BS2 = State()
    BS3 = State()


class SOSState(StatesGroup):
    SS1 = State()
    SS2 = State()


class PromoStates(StatesGroup):
    P1 = State()


class OrdersStates(StatesGroup):
    OS1 = State()
    OS2 = State()
    OS3 = State()


class ShowOrderStatusState(StatesGroup):
    SO1 = State()


class CatalogStates(StatesGroup):
    CS1 = State()
    CS2 = State()
    CS3 = State()
    CS4 = State()
    CS5 = State()
    CS6 = State()
    CS7 = State()


class SetQiwiToken(StatesGroup):
    SQT1 = State()


class BlockQiwi(StatesGroup):
    BQ1 = State()


class Transfer(StatesGroup):
    T1 = State()
    T2 = State()
    T3 = State()
