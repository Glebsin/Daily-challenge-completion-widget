from datetime import datetime, timezone
from ossapi import Ossapi
from widget_templates import DEFAULT_TEMPLATE, ALTERNATIVE_TEMPLATE
from saveload_settings_utils import save_settings as utils_save_settings

UPDATE_INTERVALS = [
    (5 * 60 * 1000, "5 minutes"),
    (10 * 60 * 1000, "10 minutes"),
    (15 * 60 * 1000, "15 minutes"),
    (30 * 60 * 1000, "30 minutes"),
    (60 * 60 * 1000, "60 minutes"),
]

def calculate_days_since_start():
    now = datetime.now(timezone.utc)
    date_only = now.strftime('%Y-%m-%d')
    return date_only

def get_daily_streak(
    osu_client_id,
    osu_client_secret,
    osu_username,
    enable_logging,
    calculate_days_since_start,
    Ossapi,
    last_update_time
):
    use_alternative_template = False
    new_last_update_time = last_update_time
    daily_streak_current = 0
    weekly_streak_current = 0
    daily_streak_best = 0
    weekly_streak_best = 0
    top_10p_placements = 0
    top_50p_placements = 0
    try:
        if not osu_client_id or not osu_client_secret or not osu_username:
            if enable_logging:
                print("[osu!api] Skipping API request - missing credentials")
            use_alternative_template = False
            return '0d', use_alternative_template, new_last_update_time, daily_streak_current, weekly_streak_current, daily_streak_best, weekly_streak_best, top_10p_placements, top_50p_placements
        if enable_logging:
            print(f"[osu!api] All credentials present, sending request for user {osu_username}")
        try:
            api = Ossapi(osu_client_id, osu_client_secret)
            user = api.user(osu_username)
            streak_value = user.daily_challenge_user_stats.playcount
            last_update_date = user.daily_challenge_user_stats.last_update
            daily_streak_current = user.daily_challenge_user_stats.daily_streak_current
            weekly_streak_current = user.daily_challenge_user_stats.weekly_streak_current
            daily_streak_best = user.daily_challenge_user_stats.daily_streak_best
            weekly_streak_best = user.daily_challenge_user_stats.weekly_streak_best
            top_10p_placements = getattr(user.daily_challenge_user_stats, "top_10p_placements", 0)
            top_50p_placements = getattr(user.daily_challenge_user_stats, "top_50p_placements", 0)
            if isinstance(last_update_date, str):
                last_update_str = last_update_date.split(" ")[0]
            elif isinstance(last_update_date, datetime):
                last_update_str = last_update_date.strftime('%Y-%m-%d')
            else:
                last_update_str = None
            today_str = calculate_days_since_start()
            if enable_logging:
                print(f"[Widget] Today: {today_str}, Last update: {last_update_str}")
            try:
                today_dt = datetime.strptime(today_str, '%Y-%m-%d')
                last_update_dt = datetime.strptime(last_update_str, '%Y-%m-%d')
                date_diff = (today_dt - last_update_dt).days
            except Exception as e:
                if enable_logging:
                    print(f"[Widget] Date calculation error: {e}")
                date_diff = 0
            if date_diff == 0:
                use_alternative_template = True
            else:
                use_alternative_template = False
            new_last_update_time = datetime.now(timezone.utc)
            return f"{streak_value}d", use_alternative_template, new_last_update_time, daily_streak_current, weekly_streak_current, daily_streak_best, weekly_streak_best, top_10p_placements, top_50p_placements
        except Exception as api_error:
            if enable_logging:
                print(f"[osu!api] API request error: {api_error}")
            use_alternative_template = False
            return '0d', use_alternative_template, new_last_update_time, daily_streak_current, weekly_streak_current, daily_streak_best, weekly_streak_best, top_10p_placements, top_50p_placements
    except Exception as e:
        if enable_logging:
            print(f"[osu!api] Error getting daily streak: {e}")
        use_alternative_template = False
        return '0d', use_alternative_template, new_last_update_time, daily_streak_current, weekly_streak_current, daily_streak_best, weekly_streak_best, top_10p_placements, top_50p_placements

def get_streak_colour_var(streak_value):
    try:
        streak = int(str(streak_value).replace('d', '')) if streak_value is not None else 0
    except (ValueError, TypeError):
        return '--level-tier-iron'
    if streak >= 1080:
        return '--level-tier-lustrous'
    elif streak >= 720:
        return '--level-tier-radiant'
    elif streak >= 360:
        return '--level-tier-rhodium'
    elif streak >= 180:
        return '--level-tier-platinum'
    elif streak >= 90:
        return '--level-tier-gold'
    elif streak >= 30:
        return '--level-tier-silver'
    elif streak >= 15:
        return '--level-tier-bronze'
    else:
        return '--level-tier-iron'

def update_streak(widget):
    (streak_value, use_alternative_template, new_last_update_time, daily_streak_current, weekly_streak_current, daily_streak_best, weekly_streak_best, top_10p_placements, top_50p_placements) = get_daily_streak(
        osu_client_id=widget.osu_client_id,
        osu_client_secret=widget.osu_client_secret,
        osu_username=widget.osu_username,
        enable_logging=widget.enable_logging,
        calculate_days_since_start=calculate_days_since_start,
        Ossapi=Ossapi,
        last_update_time=widget.last_update_time
    )
    widget.use_alternative_template = use_alternative_template
    widget.last_update_time = new_last_update_time
    widget.popup_streak_value = streak_value
    widget.popup_daily_streak_current = daily_streak_current
    widget.popup_weekly_streak_current = weekly_streak_current
    widget.popup_daily_streak_best = daily_streak_best
    widget.popup_weekly_streak_best = weekly_streak_best
    widget.popup_top_10p_placements = top_10p_placements
    widget.popup_top_50p_placements = top_50p_placements
    streak_colour_var = get_streak_colour_var(streak_value)
    current_template = ALTERNATIVE_TEMPLATE if widget.use_alternative_template else DEFAULT_TEMPLATE
    local_time = datetime.now().astimezone()
    local_time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
    html_content = current_template.format(
        current_time=local_time_str,
        current_user=widget.osu_username,
        daily_streak=streak_value,
        streak_colour_var=streak_colour_var
    )
    additional_style = """
        * {
            -webkit-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
            user-select: none !important;
        }
        ::selection {
            background: transparent !important;
        }
    """
    html_content = html_content.replace('</style>', additional_style + '</style>')
    if hasattr(widget, 'webView'):
        widget.webView.setHtml(html_content)
        if widget.enable_logging:
            print(f"[Widget] Streak value updated: {streak_value}")
            print(f"[Widget] Using {'ALTERNATIVE' if widget.use_alternative_template else 'DEFAULT'} template")
    widget.update_menu_time_action()

def update_osu_settings(widget, client_id=None, client_secret=None, username=None):
    settings_changed = False
    updated = False
    if client_id is not None and client_id != widget.osu_client_id:
        widget.osu_client_id = client_id
        settings_changed = True
        updated = True
    if client_secret is not None and client_secret != widget.osu_client_secret:
        widget.osu_client_secret = client_secret
        settings_changed = True
        updated = True
    if username is not None and username != widget.osu_username:
        widget.osu_username = username
        settings_changed = True
        updated = True
    if widget.osu_client_id and widget.osu_client_secret and widget.osu_username and updated:
        if widget.enable_logging:
            print("[osu!api] Credentials updated, calling update_streak")
        widget.update_streak()
    if settings_changed:
        current_pos = {
            'x': int(widget.geometry().x()),
            'y': int(widget.geometry().y())
        }
        widget.settings['position'] = current_pos
        widget.save_settings()