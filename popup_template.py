HTML_POPUP_TEMPLATE = """<!DOCTYPE html>
<html>
  <head>
    <style>
      @font-face {{
        font-family: 'DCCW';
        src: url(data:font/opentype;base64,{font_base64}) format("opentype");
        font-weight: normal;
        font-style: normal;
      }}
      html, body {{
        overflow: hidden !important;
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        font-family: 'DCCW', var(--font-default-override, var(--font-default));
      }}
      body::-webkit-scrollbar, html::-webkit-scrollbar {{
        display: none !important;
        width: 0 !important;
        background: transparent !important;
      }}
      .qtip {{
        box-shadow: none;
        direction: ltr;
        font-size: 10.5px;
        padding: 0;
        position: absolute;
      }}
      :root {{
        --font-default: 'DCCW';
        --navbar-height: 50px;
        --scroll-padding-top: calc(var(--navbar-height) + 1em + var(--scroll-padding-top-extra, 0px));
        --page-gutter: 10px;
      }}
      body {{
        --base-hue: var(--base-hue-override, var(--base-hue-default));
        --base-hue-deg: calc(var(--base-hue)*1deg);
        --level-tier-iron: #bab3ab, #bab3ab;
        --level-tier-bronze: #b88f7a, #855c47;
        --level-tier-silver: #e0e0eb, #a3a3c2;
        --level-tier-gold: #f0e4a8, #e0c952;
        --level-tier-platinum: #a8f0ef, #52e0df;
        --level-tier-rhodium: #d9f8d3, #a0cf96;
        --level-tier-radiant: #97dcff, #ed82ff;
        --level-tier-lustrous: #ffe600, #ed82ff;
        font-family: 'DCCW', var(--font-default-override, var(--font-default));
      }}
      .daily-challenge-popup {{
        background: hsl(var(--hsl-b4));
        border-radius: 20px;
        font-size: 12px;
      }}
      .daily-challenge-popup__content {{
        display: grid;
        gap: 10px;
        padding: 15px;
      }}
      .daily-challenge-popup__content--main {{
        grid-template-columns: 1fr auto;
      }}
      .daily-challenge-popup__content--top {{
        background: hsl(var(--hsl-b5));
        border-top-left-radius: inherit;
        border-top-right-radius: inherit;
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
      }}
      .daily-challenge-popup__row {{
        display: contents;
      }}
      .daily-challenge-popup__value {{
        --colour: hsl(var(--hsl-c2));
        color: hsl(var(--hsl-c2));
      }}
      .daily-challenge-popup__value--fancy {{
        -webkit-background-clip: text;
        background-clip: text;
        background-image: linear-gradient(var(--colour));
        color: transparent;
      }}
      .daily-challenge-popup__value--top {{
        font-size: 40px;
        font-weight: 300;
      }}
      .qtip {{
        color: hsl(var(--hsl-c1));
      }}
      .qtip--daily-challenge {{
        background: transparent;
        border: none;
        line-height: normal;
        max-width: none;
        min-width: 300px;
      }}
      .qtip--daily-challenge .qtip-content {{
        padding: 0 0 5px;
      }}
      body {{
        --hsl-p: var(--base-hue), 100%, 50%;
        --hsl-h1: var(--base-hue), 100%, 70%;
        --hsl-h2: var(--base-hue), 50%, 45%;
        --hsl-c1: var(--base-hue), 40%, 100%;
        --hsl-c2: var(--base-hue), 40%, 90%;
        --hsl-l1: var(--base-hue), 40%, 80%;
        --hsl-l2: var(--base-hue), 40%, 75%;
        --hsl-l3: var(--base-hue), 40%, 70%;
        --hsl-l4: var(--base-hue), 40%, 50%;
        --hsl-d1: var(--base-hue), 20%, 35%;
        --hsl-d2: var(--base-hue), 20%, 30%;
        --hsl-d3: var(--base-hue), 20%, 25%;
        --hsl-d4: var(--base-hue), 20%, 20%;
        --hsl-d5: var(--base-hue), 20%, 15%;
        --hsl-d6: var(--base-hue), 20%, 10%;
        --hsl-f1: var(--base-hue), 10%, 60%;
        --hsl-b1: var(--base-hue), 10%, 40%;
        --hsl-b2: var(--base-hue), 10%, 30%;
        --hsl-b3: var(--base-hue), 10%, 25%;
        --hsl-b4: var(--base-hue), 10%, 20%;
        --hsl-b5: var(--base-hue), 10%, 15%;
        --hsl-b6: var(--base-hue), 10%, 10%;
        --c-saturation-1: 100%;
        --c-saturation-2: 80%;
        --c-saturation-3: 60%;
        --c-saturation-4: 40%;
        --c-lightness-1: 70%;
        --c-lightness-2: 60%;
        --c-lightness-3: 50%;
        --c-lightness-4: 30%;
        --colour-pink-hue: 333;
        --hsl-pink-1: var(--colour-pink-hue), var(--c-saturation-1), var(--c-lightness-1);
        --hsl-pink-2: var(--colour-pink-hue), var(--c-saturation-2), var(--c-lightness-2);
        --hsl-pink-3: var(--colour-pink-hue), var(--c-saturation-3), var(--c-lightness-3);
        --hsl-pink-4: var(--colour-pink-hue), var(--c-saturation-4), var(--c-lightness-4);
        --colour-purple-hue: 255;
        --hsl-purple-1: var(--colour-purple-hue), var(--c-saturation-1), var(--c-lightness-1);
        --hsl-purple-2: var(--colour-purple-hue), var(--c-saturation-2), var(--c-lightness-2);
        --hsl-purple-3: var(--colour-purple-hue), var(--c-saturation-3), var(--c-lightness-3);
        --hsl-purple-4: var(--colour-purple-hue), var(--c-saturation-4), var(--c-lightness-4);
        --colour-blue-hue: 200;
        --hsl-blue-1: var(--colour-blue-hue), var(--c-saturation-1), var(--c-lightness-1);
        --hsl-blue-2: var(--colour-blue-hue), var(--c-saturation-2), var(--c-lightness-2);
        --hsl-blue-3: var(--colour-blue-hue), var(--c-saturation-3), var(--c-lightness-3);
        --hsl-blue-4: var(--colour-blue-hue), var(--c-saturation-4), var(--c-lightness-4);
        --colour-green-hue: 125;
        --hsl-green-1: var(--colour-green-hue), var(--c-saturation-1), var(--c-lightness-1);
        --hsl-green-2: var(--colour-green-hue), var(--c-saturation-2), var(--c-lightness-2);
        --hsl-green-3: var(--colour-green-hue), var(--c-saturation-3), var(--c-lightness-3);
        --hsl-green-4: var(--colour-green-hue), var(--c-saturation-4), var(--c-lightness-4);
        --colour-lime-hue: 90;
        --hsl-lime-1: var(--colour-lime-hue), var(--c-saturation-1), var(--c-lightness-1);
        --hsl-lime-2: var(--colour-lime-hue), var(--c-saturation-2), var(--c-lightness-2);
        --hsl-lime-3: var(--colour-lime-hue), var(--c-saturation-3), var(--c-lightness-3);
        --hsl-lime-4: var(--colour-lime-hue), var(--c-saturation-4), var(--c-lightness-4);
        --colour-orange-hue: 45;
        --hsl-orange-1: var(--colour-orange-hue), var(--c-saturation-1), var(--c-lightness-1);
        --hsl-orange-2: var(--colour-orange-hue), var(--c-saturation-2), var(--c-lightness-2);
        --hsl-orange-3: var(--colour-orange-hue), var(--c-saturation-3), var(--c-lightness-3);
        --hsl-orange-4: var(--colour-orange-hue), var(--c-saturation-4), var(--c-lightness-4);
        --colour-red-hue: 360;
        --hsl-red-1: var(--colour-red-hue), var(--c-saturation-1), var(--c-lightness-1);
        --hsl-red-2: var(--colour-red-hue), var(--c-saturation-2), var(--c-lightness-2);
        --hsl-red-3: var(--colour-red-hue), var(--c-saturation-3), var(--c-lightness-3);
        --hsl-red-4: var(--colour-red-hue), var(--c-saturation-4), var(--c-lightness-4);
        --colour-darkorange-hue: 20;
        --hsl-darkorange-1: var(--colour-darkorange-hue), var(--c-saturation-1), var(--c-lightness-1);
        --hsl-darkorange-2: var(--colour-darkorange-hue), var(--c-saturation-2), var(--c-lightness-2);
        --hsl-darkorange-3: var(--colour-darkorange-hue), var(--c-saturation-3), var(--c-lightness-3);
        --hsl-darkorange-4: var(--colour-darkorange-hue), var(--c-saturation-4), var(--c-lightness-4);
      }}
    </style>
  </head>
  <body class="t-section osu-layout osu-layout--body osu-layout--body-lazer js-animate-nav" style="--base-hue-default:333;--base-hue-override:333">
    <div id="qtip-0" class="qtip qtip-default qtip--daily-challenge qtip-fixed qtip-focus qtip-pos-tl qtip-pos-bl">
      <div class="qtip-tip" style="display:none"></div>
      <div class="qtip-content" id="qtip-0-content" aria-atomic="true">
        <div class="daily-challenge-popup">
          <div class="daily-challenge-popup__content daily-challenge-popup__content--top">
            <div class="daily-challenge-popup__top-entry">
              <div class="daily-challenge-popup__top-title">Total Participation</div>
              <div class="daily-challenge-popup__value daily-challenge-popup__value--fancy daily-challenge-popup__value--top" style="--colour:var({streak_colour_var})">{streak_value}</div>
            </div>
            <div class="daily-challenge-popup__top-entry">
              <div class="daily-challenge-popup__top-title">Current Daily Streak</div>
              <div class="daily-challenge-popup__value daily-challenge-popup__value--fancy daily-challenge-popup__value--top" style="--colour:var({daily_streak_colour_var})">{daily_streak_current}</div>
            </div>
            <div class="daily-challenge-popup__top-entry">
              <div class="daily-challenge-popup__top-title">Current Weekly Streak</div>
              <div class="daily-challenge-popup__value daily-challenge-popup__value--fancy daily-challenge-popup__value--top" style="--colour:var({weekly_streak_colour_var})">{weekly_streak_current}</div>
            </div>
          </div>
          <div class="daily-challenge-popup__content daily-challenge-popup__content--main">
            <div class="daily-challenge-popup__row">
              <div class="daily-challenge-popup__key">Best Daily Streak</div>
              <div class="daily-challenge-popup__value daily-challenge-popup__value--fancy" style="--colour:var({daily_streak_best_colour_var})">{daily_streak_best}</div>
            </div>
            <div class="daily-challenge-popup__row">
              <div class="daily-challenge-popup__key">Best Weekly Streak</div>
              <div class="daily-challenge-popup__value daily-challenge-popup__value--fancy daily-challenge-popup__value--weekly" style="--colour:var({weekly_streak_best_colour_var})">{weekly_streak_best}</div>
            </div>
            <div class="daily-challenge-popup__row">
              <div class="daily-challenge-popup__key">Top 10% Placements</div>
              <div class="daily-challenge-popup__value">{top_10p_placements}</div>
            </div>
            <div class="daily-challenge-popup__row">
              <div class="daily-challenge-popup__key">Top 50% Placements</div>
              <div class="daily-challenge-popup__value">{top_50p_placements}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
"""