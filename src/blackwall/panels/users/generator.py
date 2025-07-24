from blackwall.api import user
from blackwall.panels.panel_mode import PanelMode
from blackwall.panels.users.user import PanelUser, UserInfo


def get_user_objects_for_panel(username: str) -> PanelUser:
    new_user_panel = PanelUser()

    user_dict = user.get_user(username)

    base_traits = user.BaseUserTraits.from_dict(prefix="base",source=user_dict["profile"]["base"])

    new_user_panel.user_info = UserInfo(
        base_traits=base_traits,
        username=username,
        mode=PanelMode.edit,
    )

    if 'profile' in user_dict and 'tso' in user_dict['profile']:
        new_user_panel.user_info.tso_traits = user.TSOUserTraits.from_dict(prefix="tso",source=user_dict["profile"]["tso"])

    if 'profile' in user_dict and 'omvs' in user_dict['profile']:
        new_user_panel.user_info.omvs_traits = user.OMVSUserTraits.from_dict(prefix="omvs",source=user_dict["profile"]["omvs"])

    if 'profile' in user_dict and 'nds' in user_dict['profile']:
        new_user_panel.user_info.nds_traits = user.NDSUserTraits.from_dict(prefix="nds",source=user_dict["profile"]["nds"])

    if 'profile' in user_dict and 'cics' in user_dict['profile']:
        new_user_panel.user_info.cics_traits = user.CICSUserTraits.from_dict(prefix="cics",source=user_dict["profile"]["cics"])

    if 'profile' in user_dict and 'netview' in user_dict['profile']:
        new_user_panel.user_info.netview_traits = user.NetviewUserTraits.from_dict(prefix="netview",source=user_dict["profile"]["netview"])

    if 'profile' in user_dict and 'mfa' in user_dict['profile']:
        new_user_panel.user_info.mfa_traits = user.MfaUserTraits.from_dict(prefix="mfa",source=user_dict["profile"]["mfa"])
    
    if 'profile' in user_dict and 'eim' in user_dict['profile']:
        new_user_panel.user_info.eim_traits = user.EIMUserTraits.from_dict(prefix="eim",source=user_dict["profile"]["eim"])

    if 'profile' in user_dict and 'workattr' in user_dict['profile']:
        new_user_panel.user_info.workattr_traits = user.WorkattrUserTraits.from_dict(prefix="workattr",source=user_dict["profile"]["workattr"])
    
    if 'profile' in user_dict and 'ovm' in user_dict['profile']:
        new_user_panel.user_info.ovm_traits = user.OvmUserTraits.from_dict(prefix="ovm",source=user_dict["profile"]["ovm"])

    if 'profile' in user_dict and 'dce' in user_dict['profile']:
        new_user_panel.user_info.dce_traits = user.DCEUserTraits.from_dict(prefix="dce",source=user_dict["profile"]["dce"])
    
    if 'profile' in user_dict and 'dfp' in user_dict['profile']:
        new_user_panel.user_info.dfp_traits = user.DFPUserTraits.from_dict(prefix="dfp",source=user_dict["profile"]["dfp"])

    if 'profile' in user_dict and 'operparm' in user_dict['profile']:
        new_user_panel.user_info.operparm_traits = user.OperparmUserTraits.from_dict(prefix="operparm",source=user_dict["profile"]["operparm"])

    if 'profile' in user_dict and 'proxy' in user_dict['profile']:
        new_user_panel.user_info.proxy_traits = user.ProxyUserTraits.from_dict(prefix="proxy",source=user_dict["profile"]["proxy"])
    
    if 'profile' in user_dict and 'lnotes' in user_dict['profile']:
        new_user_panel.user_info.lnotes_traits = user.LnotesUserTraits.from_dict(prefix="lnotes",source=user_dict["profile"]["lnotes"])

    if 'profile' in user_dict and 'language' in user_dict['profile']:
        new_user_panel.user_info.lang_traits = user.LanguageUserTraits.from_dict(prefix="language",source=user_dict["profile"]["language"])

    if 'profile' in user_dict and 'kerb' in user_dict['profile']:
        new_user_panel.user_info.kerb_traits = user.KerbUserTraits.from_dict(prefix="kerb",source=user_dict["profile"]["kerb"])

    return new_user_panel