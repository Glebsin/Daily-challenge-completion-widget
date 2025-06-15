DEFAULT_TEMPLATE = """
<!DOCTYPE html>
<style>
  :root {{
    --font-default: DCCW
  }}
@font-face {{
        font-family: 'DCCW';
        src: url(data:font/opentype;base64,{font_base64}) format("opentype");
        font-weight: normal;
        font-style: normal;
      }}
  html, body {{
    width: 160px;
    height: 57px;
    margin: 0;
    padding: 0;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
  }}

  body {{
    --forum-item-background-color: hsl(var(--hsl-b4));
    --forum-item-background-color-hover: hsl(var(--hsl-b3));
    --base-hue: var(--base-hue-override, var(--base-hue-default));
    --base-hue-deg: calc(var(--base-hue)*1deg);
    --level-tier-iron: #bab3ab,#bab3ab;
    --level-tier-bronze: #b88f7a,#855c47;
    --level-tier-silver: #e0e0eb,#a3a3c2;
    --level-tier-gold: #f0e4a8,#e0c952;
    --level-tier-platinum: #a8f0ef,#52e0df;
    --level-tier-rhodium: #d9f8d3,#a0cf96;
    --level-tier-radiant: #97dcff,#ed82ff;
    --level-tier-lustrous: #ffe600,#ed82ff;

    font-family: var(--font-default-override, var(--font-default));
    position: static;
    margin: 0;
    background: transparent !important;
    -webkit-user-select: none;
    user-select: none;
    overflow: hidden;

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
  }}

  .osu-page {{
    background: transparent !important;
    width: 160px;
    height: 57px;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
  }}

  .profile-detail__values {{
    background: transparent !important;
    width: 160px;
    height: 57px;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
  }}

  .daily-challenge {{
    background: hsl(var(--hsl-b4));
    border: 2px solid transparent;
    border-radius: 6px;
    display: flex;
    padding: 1px;
    position: relative;
    width: fit-content;
    margin: 3px;
    margin-top: 3px;
  }}

  .daily-challenge__name {{
    font-size: 12px;
    padding: 0 5px;
    color: white;
  }}

  .daily-challenge__value {{
    --colour: var({streak_colour_var});
    background: linear-gradient(180deg, var(--colour));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
  }}

  .daily-challenge__value-box {{
    background: hsl(var(--hsl-b6));
    border-radius: 3px;
    padding: 5px 10px;
    width: 67.75px;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
  }}
</style></head>
<body style="--base-hue-default: 333; --base-hue-override: 333">
  <div class="osu-page">
    <div class="profile-detail__values">
      <div class="daily-challenge">
        <div class="daily-challenge__name">
          <div>Daily</div>
          <div>Challenge</div>
        </div>
        <div class="daily-challenge__value-box">
          <div class="daily-challenge__value" title="Last updated: {current_time}&#13;User: {current_user}">{daily_streak}</div>
        </div>
      </div>
    </div>
  </div>
</body></html>
"""

ALTERNATIVE_TEMPLATE = """
<!DOCTYPE html>
<style>
:root {{
    --font-default: DCCW
}}
@font-face {{
        font-family: 'DCCW';
        src: url(data:font/opentype;base64,{font_base64}) format("opentype");
        font-weight: normal;
        font-style: normal;
      }}
html, body {{
    width: 160px;
    height: 57px;
    margin: 0;
    padding: 0;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}}

body {{
    --forum-item-background-color: hsl(var(--hsl-b4));
    --forum-item-background-color-hover: hsl(var(--hsl-b3));
    --base-hue: var(--base-hue-override,var(--base-hue-default));
    --base-hue-deg: calc(var(--base-hue)*1deg);
    --level-tier-iron: #bab3ab,#bab3ab;
    --level-tier-bronze: #b88f7a,#855c47;
    --level-tier-silver: #e0e0eb,#a3a3c2;
    --level-tier-gold: #f0e4a8,#e0c952;
    --level-tier-platinum: #a8f0ef,#52e0df;
    --level-tier-rhodium: #d9f8d3,#a0cf96;
    --level-tier-radiant: #97dcff,#ed82ff;
    --level-tier-lustrous: #ffe600,#ed82ff;

    font-family: var(--font-default-override,var(--font-default));
    margin: 0;
    position: static
}}

.daily-challenge {{
    background: hsl(var(--hsl-b4));
    border: 2px solid transparent;
    border-radius: 6px;
    display: flex;
    padding: 1px;
    position: relative
}}

.daily-challenge--played-today {{
    border-color: hsl(var(--hsl-lime-1))
}}

.daily-challenge--played-today:before {{
    -moz-osx-font-smoothing: grayscale;
    -webkit-font-smoothing: antialiased;
    align-items: center;
    background-color: hsl(var(--hsl-lime-1));
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 512 512' fill='currentColor'%3E%3Cpath d='M173.9 439.4l-166.4-166.4c-10-10-10-26.2 0-36.2l36.2-36.2c10-10 26.2-10 36.2 0L192 312.7 432.1 72.6c10-10 26.2-10 36.2 0l36.2 36.2c10 10 10 26.2 0 36.2l-294.4 294.4c-10 10-26.2 10-36.2 0z'/%3E%3C/svg%3E");
    background-position: center;
    background-repeat: no-repeat;
    background-size: 8px 8px; 
    border-radius: 50%;
    color: hsl(var(--hsl-b6));
    content: '';
    display: inline-block;
    height: 16px;
    position: absolute;
    right: 0;
    top: 0;
    transform: translate(50%,-50%);
    width: 16px;
}}

.daily-challenge__name {{
    font-size: 12px;
    padding: 0 5px;
    color: white
}}

.daily-challenge__value {{
    --colour: var({streak_colour_var});
    -webkit-background-clip: text;
    background-image: linear-gradient(180deg, var(--colour));
    background-clip: text;
    color: transparent;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
}}

.daily-challenge__value-box {{
    background: hsl(var(--hsl-b6));
    border-radius: 3px;
    padding: 5px 10px;
    width: 67.75px;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}}

.profile-detail {{
    --gutter: 10px;
    background-color: transparent !important;
    display: grid;
    gap: 10px;
    padding: 10px var(--gutter)
}}

.profile-detail__values {{
    display: flex;
}}

body {{
    --hsl-p: var(--base-hue),100%,50%;
    --hsl-h1: var(--base-hue),100%,70%;
    --hsl-h2: var(--base-hue),50%,45%;
    --hsl-c1: var(--base-hue),40%,100%;
    --hsl-c2: var(--base-hue),40%,90%;
    --hsl-l1: var(--base-hue),40%,80%;
    --hsl-l2: var(--base-hue),40%,75%;
    --hsl-l3: var(--base-hue),40%,70%;
    --hsl-l4: var(--base-hue),40%,50%;
    --hsl-d1: var(--base-hue),20%,35%;
    --hsl-d2: var(--base-hue),20%,30%;
    --hsl-d3: var(--base-hue),20%,25%;
    --hsl-d4: var(--base-hue),20%,20%;
    --hsl-d5: var(--base-hue),20%,15%;
    --hsl-d6: var(--base-hue),20%,10%;
    --hsl-f1: var(--base-hue),10%,60%;
    --hsl-b1: var(--base-hue),10%,40%;
    --hsl-b2: var(--base-hue),10%,30%;
    --hsl-b3: var(--base-hue),10%,25%;
    --hsl-b4: var(--base-hue),10%,20%;
    --hsl-b5: var(--base-hue),10%,15%;
    --hsl-b6: var(--base-hue),10%,10%;
    --c-saturation-1: 100%;
    --c-saturation-2: 80%;
    --c-saturation-3: 60%;
    --c-saturation-4: 40%;
    --c-lightness-1: 70%;
    --c-lightness-2: 60%;
    --c-lightness-3: 50%;
    --c-lightness-4: 30%;
    --colour-pink-hue: 333;
    --hsl-pink-1: var(--colour-pink-hue),var(--c-saturation-1),var(--c-lightness-1);
    --hsl-pink-2: var(--colour-pink-hue),var(--c-saturation-2),var(--c-lightness-2);
    --hsl-pink-3: var(--colour-pink-hue),var(--c-saturation-3),var(--c-lightness-3);
    --hsl-pink-4: var(--colour-pink-hue),var(--c-saturation-4),var(--c-lightness-4);
    --colour-purple-hue: 255;
    --hsl-purple-1: var(--colour-purple-hue),var(--c-saturation-1),var(--c-lightness-1);
    --hsl-purple-2: var(--colour-purple-hue),var(--c-saturation-2),var(--c-lightness-2);
    --hsl-purple-3: var(--colour-purple-hue),var(--c-saturation-3),var(--c-lightness-3);
    --hsl-purple-4: var(--colour-purple-hue),var(--c-saturation-4),var(--c-lightness-4);
    --colour-blue-hue: 200;
    --hsl-blue-1: var(--colour-blue-hue),var(--c-saturation-1),var(--c-lightness-1);
    --hsl-blue-2: var(--colour-blue-hue),var(--c-saturation-2),var(--c-lightness-2);
    --hsl-blue-3: var(--colour-blue-hue),var(--c-saturation-3),var(--c-lightness-3);
    --hsl-blue-4: var(--colour-blue-hue),var(--c-saturation-4),var(--c-lightness-4);
    --colour-green-hue: 125;
    --hsl-green-1: var(--colour-green-hue),var(--c-saturation-1),var(--c-lightness-1);
    --hsl-green-2: var(--colour-green-hue),var(--c-saturation-2),var(--c-lightness-2);
    --hsl-green-3: var(--colour-green-hue),var(--c-saturation-3),var(--c-lightness-3);
    --hsl-green-4: var(--colour-green-hue),var(--c-saturation-4),var(--c-lightness-4);
    --colour-lime-hue: 90;
    --hsl-lime-1: var(--colour-lime-hue),var(--c-saturation-1),var(--c-lightness-1);
    --hsl-lime-2: var(--colour-lime-hue),var(--c-saturation-2),var(--c-lightness-2);
    --hsl-lime-3: var(--colour-lime-hue),var(--c-saturation-3),var(--c-lightness-3);
    --hsl-lime-4: var(--colour-lime-hue),var(--c-saturation-4),var(--c-lightness-4);
    --colour-orange-hue: 45;
    --hsl-orange-1: var(--colour-orange-hue),var(--c-saturation-1),var(--c-lightness-1);
    --hsl-orange-2: var(--colour-orange-hue),var(--c-saturation-2),var(--c-lightness-2);
    --hsl-orange-3: var(--colour-orange-hue),var(--c-saturation-3),var(--c-lightness-3);
    --hsl-orange-4: var(--colour-orange-hue),var(--c-saturation-4),var(--c-lightness-4);
    --colour-red-hue: 360;
    --hsl-red-1: var(--colour-red-hue),var(--c-saturation-1),var(--c-lightness-1);
    --hsl-red-2: var(--colour-red-hue),var(--c-saturation-2),var(--c-lightness-2);
    --hsl-red-3: var(--colour-red-hue),var(--c-saturation-3),var(--c-lightness-3);
    --hsl-red-4: var(--colour-red-hue),var(--c-saturation-4),var(--c-lightness-4);
    --colour-darkorange-hue: 20;
    --hsl-darkorange-1: var(--colour-darkorange-hue),var(--c-saturation-1),var(--c-lightness-1);
    --hsl-darkorange-2: var(--colour-darkorange-hue),var(--c-saturation-2),var(--c-lightness-2);
    --hsl-darkorange-3: var(--colour-darkorange-hue),var(--c-saturation-3),var(--c-lightness-3);
    --hsl-darkorange-4: var(--colour-darkorange-hue),var(--c-saturation-4),var(--c-lightness-4)
}}

</style>
</head>
<body class="t-section osu-layout osu-layout--body osu-layout--body-lazer js-animate-nav" style="--base-hue-default: 333; --base-hue-override: 333">
    <div class="profile-detail">
          <div class="profile-detail__chart-numbers profile-detail__chart-numbers--top">
            <div class="profile-detail__values">
              <div class="daily-challenge daily-challenge--played-today" data-hasqtip="2" aria-describedby="qtip-2">
                <div class="daily-challenge__name">
                  <div>Daily</div>
                  <div>Challenge</div>
                </div>
                <div class="daily-challenge__value-box">
                  <div class="daily-challenge__value" style="--colour: var({streak_colour_var});" title="Last updated: {current_time}&#13;User: {current_user}">{daily_streak}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
</body></html>
"""