from datetime import datetime, timezone

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
    try:
        if not osu_client_id or not osu_client_secret or not osu_username:
            if enable_logging:
                print("[osu!api] Skipping API request - missing credentials")
            use_alternative_template = False
            return '0d', use_alternative_template, new_last_update_time
        if enable_logging:
            print(f"[osu!api] All credentials present, sending request for user {osu_username}")
        try:
            api = Ossapi(osu_client_id, osu_client_secret)
            user = api.user(osu_username)
            streak_value = user.daily_challenge_user_stats.playcount
            last_update_date = user.daily_challenge_user_stats.last_update
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
            return f"{streak_value}d", use_alternative_template, new_last_update_time
        except Exception as api_error:
            if enable_logging:
                print(f"[osu!api] API request error: {api_error}")
            use_alternative_template = False
            return '0d', use_alternative_template, new_last_update_time
    except Exception as e:
        if enable_logging:
            print(f"[osu!api] Error getting daily streak: {e}")
        use_alternative_template = False
        return '0d', use_alternative_template, new_last_update_time