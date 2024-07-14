from surprise import Dataset


def get_Iu(uid: str, trainset: Dataset) -> int:
    """
    Return the number of items rated by given user.

    Parameters
    ----------
    uid: str
        The user ID
    trainset: Dataset
        The trainset

    Returns
    -------
    int
        The number of items rated by the user
    """
    try:
        return len(trainset.ur[trainset.to_inner_uid(uid)])
    except ValueError:  # user was not part of the trainset
        return 0


def get_Ui(iid: str, trainset: Dataset) -> int:
    """
    Return number of users that have rated given item.

    Parameters
    ----------
    iid: str
        The item ID
    trainset: Dataset
        The trainset

    Returns
    -------
    int
        The number of users that have rated the item.
    """
    try:
        return len(trainset.ir[trainset.to_inner_iid(iid)])
    except ValueError:
        return 0
