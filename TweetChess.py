import chess
import chess.svg
import json
import time
import random
from twitterAPI import TwitterAPI
from datetime import date, datetime, timedelta


global TAPI
TAPI = TwitterAPI()

games_file = "ChessGames.json"
games_list = {}


#Create a new chess game related to a user and set the waiting turn
def start_game(user, move_time):
    game = {
        "tweetaccount" : user,
        "playing" : True,
        "side" : True,
        "board" : "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "boardsvg" : '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.2" baseProfile="tiny" viewBox="0 0 390 390"><desc><pre>r n b q k b n r\np p p p p p p p\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\nP P P P P P P P\nR N B Q K B N R</pre></desc><defs><g id="white-pawn" class="white pawn"><path d="M22.5 9c-2.21 0-4 1.79-4 4 0 .89.29 1.71.78 2.38C17.33 16.5 16 18.59 16 21c0 2.03.94 3.84 2.41 5.03-3 1.06-7.41 5.55-7.41 13.47h23c0-7.92-4.41-12.41-7.41-13.47 1.47-1.19 2.41-3 2.41-5.03 0-2.41-1.33-4.5-3.28-5.62.49-.67.78-1.49.78-2.38 0-2.21-1.79-4-4-4z" fill="#fff" stroke="#000" stroke-width="1.5" stroke-linecap="round" /></g><g id="white-knight" class="white knight" fill="none" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M 22,10 C 32.5,11 38.5,18 38,39 L 15,39 C 15,30 25,32.5 23,18" style="fill:#ffffff; stroke:#000000;" /><path d="M 24,18 C 24.38,20.91 18.45,25.37 16,27 C 13,29 13.18,31.34 11,31 C 9.958,30.06 12.41,27.96 11,28 C 10,28 11.19,29.23 10,30 C 9,30 5.997,31 6,26 C 6,24 12,14 12,14 C 12,14 13.89,12.1 14,10.5 C 13.27,9.506 13.5,8.5 13.5,7.5 C 14.5,6.5 16.5,10 16.5,10 L 18.5,10 C 18.5,10 19.28,8.008 21,7 C 22,7 22,10 22,10" style="fill:#ffffff; stroke:#000000;" /><path d="M 9.5 25.5 A 0.5 0.5 0 1 1 8.5,25.5 A 0.5 0.5 0 1 1 9.5 25.5 z" style="fill:#000000; stroke:#000000;" /><path d="M 15 15.5 A 0.5 1.5 0 1 1 14,15.5 A 0.5 1.5 0 1 1 15 15.5 z" transform="matrix(0.866,0.5,-0.5,0.866,9.693,-5.173)" style="fill:#000000; stroke:#000000;" /></g><g id="white-bishop" class="white bishop" fill="none" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><g fill="#fff" stroke-linecap="butt"><path d="M9 36c3.39-.97 10.11.43 13.5-2 3.39 2.43 10.11 1.03 13.5 2 0 0 1.65.54 3 2-.68.97-1.65.99-3 .5-3.39-.97-10.11.46-13.5-1-3.39 1.46-10.11.03-13.5 1-1.354.49-2.323.47-3-.5 1.354-1.94 3-2 3-2zM15 32c2.5 2.5 12.5 2.5 15 0 .5-1.5 0-2 0-2 0-2.5-2.5-4-2.5-4 5.5-1.5 6-11.5-5-15.5-11 4-10.5 14-5 15.5 0 0-2.5 1.5-2.5 4 0 0-.5.5 0 2zM25 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 1 1 5 0z" /></g><path d="M17.5 26h10M15 30h15m-7.5-14.5v5M20 18h5" stroke-linejoin="miter" /></g><g id="white-rook" class="white rook" fill="#fff" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 39h27v-3H9v3zM12 36v-4h21v4H12zM11 14V9h4v2h5V9h5v2h5V9h4v5" stroke-linecap="butt" /><path d="M34 14l-3 3H14l-3-3" /><path d="M31 17v12.5H14V17" stroke-linecap="butt" stroke-linejoin="miter" /><path d="M31 29.5l1.5 2.5h-20l1.5-2.5" /><path d="M11 14h23" fill="none" stroke-linejoin="miter" /></g><g id="white-queen" class="white queen" fill="#fff" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 12a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM24.5 7.5a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM41 12a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM16 8.5a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM33 9a2 2 0 1 1-4 0 2 2 0 1 1 4 0z" /><path d="M9 26c8.5-1.5 21-1.5 27 0l2-12-7 11V11l-5.5 13.5-3-15-3 15-5.5-14V25L7 14l2 12zM9 26c0 2 1.5 2 2.5 4 1 1.5 1 1 .5 3.5-1.5 1-1.5 2.5-1.5 2.5-1.5 1.5.5 2.5.5 2.5 6.5 1 16.5 1 23 0 0 0 1.5-1 0-2.5 0 0 .5-1.5-1-2.5-.5-2.5-.5-2 .5-3.5 1-2 2.5-2 2.5-4-8.5-1.5-18.5-1.5-27 0z" stroke-linecap="butt" /><path d="M11.5 30c3.5-1 18.5-1 22 0M12 33.5c6-1 15-1 21 0" fill="none" /></g><g id="white-king" class="white king" fill="none" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22.5 11.63V6M20 8h5" stroke-linejoin="miter" /><path d="M22.5 25s4.5-7.5 3-10.5c0 0-1-2.5-3-2.5s-3 2.5-3 2.5c-1.5 3 3 10.5 3 10.5" fill="#fff" stroke-linecap="butt" stroke-linejoin="miter" /><path d="M11.5 37c5.5 3.5 15.5 3.5 21 0v-7s9-4.5 6-10.5c-4-6.5-13.5-3.5-16 4V27v-3.5c-3.5-7.5-13-10.5-16-4-3 6 5 10 5 10V37z" fill="#fff" /><path d="M11.5 30c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0" /></g><g id="black-pawn" class="black pawn"><path d="M22.5 9c-2.21 0-4 1.79-4 4 0 .89.29 1.71.78 2.38C17.33 16.5 16 18.59 16 21c0 2.03.94 3.84 2.41 5.03-3 1.06-7.41 5.55-7.41 13.47h23c0-7.92-4.41-12.41-7.41-13.47 1.47-1.19 2.41-3 2.41-5.03 0-2.41-1.33-4.5-3.28-5.62.49-.67.78-1.49.78-2.38 0-2.21-1.79-4-4-4z" fill="#000" stroke="#000" stroke-width="1.5" stroke-linecap="round" /></g><g id="black-knight" class="black knight" fill="none" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M 22,10 C 32.5,11 38.5,18 38,39 L 15,39 C 15,30 25,32.5 23,18" style="fill:#000000; stroke:#000000;" /><path d="M 24,18 C 24.38,20.91 18.45,25.37 16,27 C 13,29 13.18,31.34 11,31 C 9.958,30.06 12.41,27.96 11,28 C 10,28 11.19,29.23 10,30 C 9,30 5.997,31 6,26 C 6,24 12,14 12,14 C 12,14 13.89,12.1 14,10.5 C 13.27,9.506 13.5,8.5 13.5,7.5 C 14.5,6.5 16.5,10 16.5,10 L 18.5,10 C 18.5,10 19.28,8.008 21,7 C 22,7 22,10 22,10" style="fill:#000000; stroke:#000000;" /><path d="M 9.5 25.5 A 0.5 0.5 0 1 1 8.5,25.5 A 0.5 0.5 0 1 1 9.5 25.5 z" style="fill:#ececec; stroke:#ececec;" /><path d="M 15 15.5 A 0.5 1.5 0 1 1 14,15.5 A 0.5 1.5 0 1 1 15 15.5 z" transform="matrix(0.866,0.5,-0.5,0.866,9.693,-5.173)" style="fill:#ececec; stroke:#ececec;" /><path d="M 24.55,10.4 L 24.1,11.85 L 24.6,12 C 27.75,13 30.25,14.49 32.5,18.75 C 34.75,23.01 35.75,29.06 35.25,39 L 35.2,39.5 L 37.45,39.5 L 37.5,39 C 38,28.94 36.62,22.15 34.25,17.66 C 31.88,13.17 28.46,11.02 25.06,10.5 L 24.55,10.4 z " style="fill:#ececec; stroke:none;" /></g><g id="black-bishop" class="black bishop" fill="none" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 36c3.39-.97 10.11.43 13.5-2 3.39 2.43 10.11 1.03 13.5 2 0 0 1.65.54 3 2-.68.97-1.65.99-3 .5-3.39-.97-10.11.46-13.5-1-3.39 1.46-10.11.03-13.5 1-1.354.49-2.323.47-3-.5 1.354-1.94 3-2 3-2zm6-4c2.5 2.5 12.5 2.5 15 0 .5-1.5 0-2 0-2 0-2.5-2.5-4-2.5-4 5.5-1.5 6-11.5-5-15.5-11 4-10.5 14-5 15.5 0 0-2.5 1.5-2.5 4 0 0-.5.5 0 2zM25 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 1 1 5 0z" fill="#000" stroke-linecap="butt" /><path d="M17.5 26h10M15 30h15m-7.5-14.5v5M20 18h5" stroke="#fff" stroke-linejoin="miter" /></g><g id="black-rook" class="black rook" fill="#000" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 39h27v-3H9v3zM12.5 32l1.5-2.5h17l1.5 2.5h-20zM12 36v-4h21v4H12z" stroke-linecap="butt" /><path d="M14 29.5v-13h17v13H14z" stroke-linecap="butt" stroke-linejoin="miter" /><path d="M14 16.5L11 14h23l-3 2.5H14zM11 14V9h4v2h5V9h5v2h5V9h4v5H11z" stroke-linecap="butt" /><path d="M12 35.5h21M13 31.5h19M14 29.5h17M14 16.5h17M11 14h23" fill="none" stroke="#fff" stroke-width="1" stroke-linejoin="miter" /></g><g id="black-queen" class="black queen" fill="#000" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><g fill="#000" stroke="none"><circle cx="6" cy="12" r="2.75" /><circle cx="14" cy="9" r="2.75" /><circle cx="22.5" cy="8" r="2.75" /><circle cx="31" cy="9" r="2.75" /><circle cx="39" cy="12" r="2.75" /></g><path d="M9 26c8.5-1.5 21-1.5 27 0l2.5-12.5L31 25l-.3-14.1-5.2 13.6-3-14.5-3 14.5-5.2-13.6L14 25 6.5 13.5 9 26zM9 26c0 2 1.5 2 2.5 4 1 1.5 1 1 .5 3.5-1.5 1-1.5 2.5-1.5 2.5-1.5 1.5.5 2.5.5 2.5 6.5 1 16.5 1 23 0 0 0 1.5-1 0-2.5 0 0 .5-1.5-1-2.5-.5-2.5-.5-2 .5-3.5 1-2 2.5-2 2.5-4-8.5-1.5-18.5-1.5-27 0z" stroke-linecap="butt" /><path d="M11 38.5a35 35 1 0 0 23 0" fill="none" stroke-linecap="butt" /><path d="M11 29a35 35 1 0 1 23 0M12.5 31.5h20M11.5 34.5a35 35 1 0 0 22 0M10.5 37.5a35 35 1 0 0 24 0" fill="none" stroke="#fff" /></g><g id="black-king" class="black king" fill="none" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22.5 11.63V6" stroke-linejoin="miter" /><path d="M22.5 25s4.5-7.5 3-10.5c0 0-1-2.5-3-2.5s-3 2.5-3 2.5c-1.5 3 3 10.5 3 10.5" fill="#000" stroke-linecap="butt" stroke-linejoin="miter" /><path d="M11.5 37c5.5 3.5 15.5 3.5 21 0v-7s9-4.5 6-10.5c-4-6.5-13.5-3.5-16 4V27v-3.5c-3.5-7.5-13-10.5-16-4-3 6 5 10 5 10V37z" fill="#000" /><path d="M20 8h5" stroke-linejoin="miter" /><path d="M32 29.5s8.5-4 6.03-9.65C34.15 14 25 18 22.5 24.5l.01 2.1-.01-2.1C20 18 9.906 14 6.997 19.85c-2.497 5.65 4.853 9 4.853 9M11.5 30c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0" stroke="#fff" /></g></defs><rect x="0" y="0" width="390" height="390" fill="#212121" /><g transform="translate(20, 0) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M23.328 10.016q-1.742 0-2.414.398-.672.398-.672 1.36 0 .765.5 1.218.508.445 1.375.445 1.196 0 1.914-.843.727-.852.727-2.258v-.32zm2.867-.594v4.992h-1.437v-1.328q-.492.797-1.227 1.18-.734.375-1.797.375-1.343 0-2.14-.75-.79-.758-.79-2.024 0-1.476.985-2.226.992-.75 2.953-.75h2.016V8.75q0-.992-.656-1.531-.649-.547-1.829-.547-.75 0-1.46.18-.711.18-1.368.539V6.062q.79-.304 1.532-.453.742-.156 1.445-.156 1.898 0 2.836.984.937.985.937 2.985z" /></g><g transform="translate(20, 375) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M23.328 10.016q-1.742 0-2.414.398-.672.398-.672 1.36 0 .765.5 1.218.508.445 1.375.445 1.196 0 1.914-.843.727-.852.727-2.258v-.32zm2.867-.594v4.992h-1.437v-1.328q-.492.797-1.227 1.18-.734.375-1.797.375-1.343 0-2.14-.75-.79-.758-.79-2.024 0-1.476.985-2.226.992-.75 2.953-.75h2.016V8.75q0-.992-.656-1.531-.649-.547-1.829-.547-.75 0-1.46.18-.711.18-1.368.539V6.062q.79-.304 1.532-.453.742-.156 1.445-.156 1.898 0 2.836.984.937.985.937 2.985z" /></g><g transform="translate(65, 0) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M24.922 10.047q0-1.586-.656-2.485-.649-.906-1.79-.906-1.14 0-1.796.906-.649.899-.649 2.485 0 1.586.649 2.492.656.898 1.797.898 1.14 0 1.789-.898.656-.906.656-2.492zm-4.89-3.055q.452-.781 1.14-1.156.695-.383 1.656-.383 1.594 0 2.586 1.266 1 1.265 1 3.328 0 2.062-1 3.328-.992 1.266-2.586 1.266-.96 0-1.656-.375-.688-.383-1.14-1.164v1.312h-1.446V2.258h1.445z" /></g><g transform="translate(65, 375) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M24.922 10.047q0-1.586-.656-2.485-.649-.906-1.79-.906-1.14 0-1.796.906-.649.899-.649 2.485 0 1.586.649 2.492.656.898 1.797.898 1.14 0 1.789-.898.656-.906.656-2.492zm-4.89-3.055q.452-.781 1.14-1.156.695-.383 1.656-.383 1.594 0 2.586 1.266 1 1.265 1 3.328 0 2.062-1 3.328-.992 1.266-2.586 1.266-.96 0-1.656-.375-.688-.383-1.14-1.164v1.312h-1.446V2.258h1.445z" /></g><g transform="translate(110, 0) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M25.96 6v1.344q-.608-.336-1.226-.5-.609-.172-1.234-.172-1.398 0-2.172.89-.773.883-.773 2.485 0 1.601.773 2.492.774.883 2.172.883.625 0 1.234-.164.618-.172 1.227-.508v1.328q-.602.281-1.25.422-.64.14-1.367.14-1.977 0-3.14-1.242-1.165-1.242-1.165-3.351 0-2.14 1.172-3.367 1.18-1.227 3.227-1.227.664 0 1.296.14.633.134 1.227.407z" /></g><g transform="translate(110, 375) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M25.96 6v1.344q-.608-.336-1.226-.5-.609-.172-1.234-.172-1.398 0-2.172.89-.773.883-.773 2.485 0 1.601.773 2.492.774.883 2.172.883.625 0 1.234-.164.618-.172 1.227-.508v1.328q-.602.281-1.25.422-.64.14-1.367.14-1.977 0-3.14-1.242-1.165-1.242-1.165-3.351 0-2.14 1.172-3.367 1.18-1.227 3.227-1.227.664 0 1.296.14.633.134 1.227.407z" /></g><g transform="translate(155, 0) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M24.973 6.992V2.258h1.437v12.156h-1.437v-1.312q-.453.78-1.149 1.164-.687.375-1.656.375-1.586 0-2.586-1.266-.992-1.266-.992-3.328 0-2.063.992-3.328 1-1.266 2.586-1.266.969 0 1.656.383.696.375 1.149 1.156zm-4.899 3.055q0 1.586.649 2.492.656.898 1.797.898 1.14 0 1.796-.898.657-.906.657-2.492 0-1.586-.657-2.485-.656-.906-1.796-.906-1.141 0-1.797.906-.649.899-.649 2.485z" /></g><g transform="translate(155, 375) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M24.973 6.992V2.258h1.437v12.156h-1.437v-1.312q-.453.78-1.149 1.164-.687.375-1.656.375-1.586 0-2.586-1.266-.992-1.266-.992-3.328 0-2.063.992-3.328 1-1.266 2.586-1.266.969 0 1.656.383.696.375 1.149 1.156zm-4.899 3.055q0 1.586.649 2.492.656.898 1.797.898 1.14 0 1.796-.898.657-.906.657-2.492 0-1.586-.657-2.485-.656-.906-1.796-.906-1.141 0-1.797.906-.649.899-.649 2.485z" /></g><g transform="translate(200, 0) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M26.555 9.68v.703h-6.61q.094 1.484.89 2.265.806.774 2.235.774.828 0 1.602-.203.781-.203 1.547-.61v1.36q-.774.328-1.586.5-.813.172-1.649.172-2.093 0-3.32-1.22-1.219-1.218-1.219-3.296 0-2.148 1.157-3.406 1.164-1.266 3.132-1.266 1.766 0 2.79 1.14 1.03 1.134 1.03 3.087zm-1.438-.422q-.015-1.18-.664-1.883-.64-.703-1.703-.703-1.203 0-1.93.68-.718.68-.828 1.914z" /></g><g transform="translate(200, 375) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M26.555 9.68v.703h-6.61q.094 1.484.89 2.265.806.774 2.235.774.828 0 1.602-.203.781-.203 1.547-.61v1.36q-.774.328-1.586.5-.813.172-1.649.172-2.093 0-3.32-1.22-1.219-1.218-1.219-3.296 0-2.148 1.157-3.406 1.164-1.266 3.132-1.266 1.766 0 2.79 1.14 1.03 1.134 1.03 3.087zm-1.438-.422q-.015-1.18-.664-1.883-.64-.703-1.703-.703-1.203 0-1.93.68-.718.68-.828 1.914z" /></g><g transform="translate(245, 0) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M25.285 2.258v1.195H23.91q-.773 0-1.078.313-.297.312-.297 1.125v.773h2.367v1.117h-2.367v7.633H21.09V6.781h-1.375V5.664h1.375v-.61q0-1.46.68-2.124.68-.672 2.156-.672z" /></g><g transform="translate(245, 375) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M25.285 2.258v1.195H23.91q-.773 0-1.078.313-.297.312-.297 1.125v.773h2.367v1.117h-2.367v7.633H21.09V6.781h-1.375V5.664h1.375v-.61q0-1.46.68-2.124.68-.672 2.156-.672z" /></g><g transform="translate(290, 0) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M24.973 9.937q0-1.562-.649-2.421-.64-.86-1.804-.86-1.157 0-1.805.86-.64.859-.64 2.421 0 1.555.64 2.415.648.859 1.805.859 1.164 0 1.804-.86.649-.859.649-2.414zm1.437 3.391q0 2.234-.992 3.32-.992 1.094-3.04 1.094-.757 0-1.429-.117-.672-.11-1.304-.344v-1.398q.632.344 1.25.508.617.164 1.257.164 1.414 0 2.118-.743.703-.734.703-2.226v-.711q-.446.773-1.141 1.156-.695.383-1.664.383-1.61 0-2.594-1.227-.984-1.226-.984-3.25 0-2.03.984-3.257.985-1.227 2.594-1.227.969 0 1.664.383t1.14 1.156V5.664h1.438z" /></g><g transform="translate(290, 375) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M24.973 9.937q0-1.562-.649-2.421-.64-.86-1.804-.86-1.157 0-1.805.86-.64.859-.64 2.421 0 1.555.64 2.415.648.859 1.805.859 1.164 0 1.804-.86.649-.859.649-2.414zm1.437 3.391q0 2.234-.992 3.32-.992 1.094-3.04 1.094-.757 0-1.429-.117-.672-.11-1.304-.344v-1.398q.632.344 1.25.508.617.164 1.257.164 1.414 0 2.118-.743.703-.734.703-2.226v-.711q-.446.773-1.141 1.156-.695.383-1.664.383-1.61 0-2.594-1.227-.984-1.226-.984-3.25 0-2.03.984-3.257.985-1.227 2.594-1.227.969 0 1.664.383t1.14 1.156V5.664h1.438z" /></g><g transform="translate(335, 0) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M26.164 9.133v5.281h-1.437V9.18q0-1.243-.485-1.86-.484-.617-1.453-.617-1.164 0-1.836.742-.672.742-.672 2.024v4.945h-1.445V2.258h1.445v4.765q.516-.789 1.211-1.18.703-.39 1.617-.39 1.508 0 2.282.938.773.93.773 2.742z" /></g><g transform="translate(335, 375) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M26.164 9.133v5.281h-1.437V9.18q0-1.243-.485-1.86-.484-.617-1.453-.617-1.164 0-1.836.742-.672.742-.672 2.024v4.945h-1.445V2.258h1.445v4.765q.516-.789 1.211-1.18.703-.39 1.617-.39 1.508 0 2.282.938.773.93.773 2.742z" /></g><g transform="translate(0, 335) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M6.754 26.996h2.578v-8.898l-2.805.562v-1.437l2.79-.563h1.578v10.336h2.578v1.328h-6.72z" /></g><g transform="translate(375, 335) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M6.754 26.996h2.578v-8.898l-2.805.562v-1.437l2.79-.563h1.578v10.336h2.578v1.328h-6.72z" /></g><g transform="translate(0, 290) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M8.195 26.996h5.508v1.328H6.297v-1.328q.898-.93 2.445-2.492 1.555-1.57 1.953-2.024.758-.851 1.055-1.437.305-.594.305-1.164 0-.93-.657-1.516-.648-.586-1.695-.586-.742 0-1.57.258-.82.258-1.758.781v-1.593q.953-.383 1.781-.578.828-.196 1.516-.196 1.812 0 2.89.906 1.079.907 1.079 2.422 0 .72-.274 1.368-.265.64-.976 1.515-.196.227-1.243 1.313-1.046 1.078-2.953 3.023z" /></g><g transform="translate(375, 290) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M8.195 26.996h5.508v1.328H6.297v-1.328q.898-.93 2.445-2.492 1.555-1.57 1.953-2.024.758-.851 1.055-1.437.305-.594.305-1.164 0-.93-.657-1.516-.648-.586-1.695-.586-.742 0-1.57.258-.82.258-1.758.781v-1.593q.953-.383 1.781-.578.828-.196 1.516-.196 1.812 0 2.89.906 1.079.907 1.079 2.422 0 .72-.274 1.368-.265.64-.976 1.515-.196.227-1.243 1.313-1.046 1.078-2.953 3.023z" /></g><g transform="translate(0, 245) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M11.434 22.035q1.132.242 1.765 1.008.64.766.64 1.89 0 1.727-1.187 2.672-1.187.946-3.375.946-.734 0-1.515-.149-.774-.14-1.602-.43V26.45q.656.383 1.438.578.78.196 1.632.196 1.485 0 2.258-.586.782-.586.782-1.703 0-1.032-.727-1.61-.719-.586-2.008-.586h-1.36v-1.297h1.423q1.164 0 1.78-.46.618-.47.618-1.344 0-.899-.64-1.375-.633-.485-1.82-.485-.65 0-1.391.141-.743.14-1.633.437V16.95q.898-.25 1.68-.375.788-.125 1.484-.125 1.797 0 2.844.82 1.046.813 1.046 2.204 0 .968-.554 1.64-.555.664-1.578.922z" /></g><g transform="translate(375, 245) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M11.434 22.035q1.132.242 1.765 1.008.64.766.64 1.89 0 1.727-1.187 2.672-1.187.946-3.375.946-.734 0-1.515-.149-.774-.14-1.602-.43V26.45q.656.383 1.438.578.78.196 1.632.196 1.485 0 2.258-.586.782-.586.782-1.703 0-1.032-.727-1.61-.719-.586-2.008-.586h-1.36v-1.297h1.423q1.164 0 1.78-.46.618-.47.618-1.344 0-.899-.64-1.375-.633-.485-1.82-.485-.65 0-1.391.141-.743.14-1.633.437V16.95q.898-.25 1.68-.375.788-.125 1.484-.125 1.797 0 2.844.82 1.046.813 1.046 2.204 0 .968-.554 1.64-.555.664-1.578.922z" /></g><g transform="translate(0, 200) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M11.016 18.035L7.03 24.262h3.985zm-.414-1.375h1.984v7.602h1.664v1.312h-1.664v2.75h-1.57v-2.75H5.75v-1.523z" /></g><g transform="translate(375, 200) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M11.016 18.035L7.03 24.262h3.985zm-.414-1.375h1.984v7.602h1.664v1.312h-1.664v2.75h-1.57v-2.75H5.75v-1.523z" /></g><g transform="translate(0, 155) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M6.719 16.66h6.195v1.328h-4.75v2.86q.344-.118.688-.172.343-.063.687-.063 1.953 0 3.094 1.07 1.14 1.07 1.14 2.899 0 1.883-1.171 2.93-1.172 1.039-3.305 1.039-.735 0-1.5-.125-.758-.125-1.57-.375v-1.586q.703.383 1.453.57.75.188 1.586.188 1.351 0 2.14-.711.79-.711.79-1.93 0-1.219-.79-1.93-.789-.71-2.14-.71-.633 0-1.266.14-.625.14-1.281.438z" /></g><g transform="translate(375, 155) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M6.719 16.66h6.195v1.328h-4.75v2.86q.344-.118.688-.172.343-.063.687-.063 1.953 0 3.094 1.07 1.14 1.07 1.14 2.899 0 1.883-1.171 2.93-1.172 1.039-3.305 1.039-.735 0-1.5-.125-.758-.125-1.57-.375v-1.586q.703.383 1.453.57.75.188 1.586.188 1.351 0 2.14-.711.79-.711.79-1.93 0-1.219-.79-1.93-.789-.71-2.14-.71-.633 0-1.266.14-.625.14-1.281.438z" /></g><g transform="translate(0, 110) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M10.137 21.863q-1.063 0-1.688.727-.617.726-.617 1.992 0 1.258.617 1.992.625.727 1.688.727 1.062 0 1.68-.727.624-.734.624-1.992 0-1.266-.625-1.992-.617-.727-1.68-.727zm3.133-4.945v1.437q-.594-.28-1.204-.43-.601-.148-1.195-.148-1.562 0-2.39 1.055-.82 1.055-.938 3.188.46-.68 1.156-1.04.696-.367 1.531-.367 1.758 0 2.774 1.07 1.023 1.063 1.023 2.899 0 1.797-1.062 2.883-1.063 1.086-2.828 1.086-2.024 0-3.094-1.547-1.07-1.555-1.07-4.5 0-2.766 1.312-4.406 1.313-1.649 3.524-1.649.593 0 1.195.117.61.118 1.266.352z" /></g><g transform="translate(375, 110) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M10.137 21.863q-1.063 0-1.688.727-.617.726-.617 1.992 0 1.258.617 1.992.625.727 1.688.727 1.062 0 1.68-.727.624-.734.624-1.992 0-1.266-.625-1.992-.617-.727-1.68-.727zm3.133-4.945v1.437q-.594-.28-1.204-.43-.601-.148-1.195-.148-1.562 0-2.39 1.055-.82 1.055-.938 3.188.46-.68 1.156-1.04.696-.367 1.531-.367 1.758 0 2.774 1.07 1.023 1.063 1.023 2.899 0 1.797-1.062 2.883-1.063 1.086-2.828 1.086-2.024 0-3.094-1.547-1.07-1.555-1.07-4.5 0-2.766 1.312-4.406 1.313-1.649 3.524-1.649.593 0 1.195.117.61.118 1.266.352z" /></g><g transform="translate(0, 65) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M6.25 16.66h7.5v.672L9.516 28.324H7.867l3.985-10.336H6.25z" /></g><g transform="translate(375, 65) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M6.25 16.66h7.5v.672L9.516 28.324H7.867l3.985-10.336H6.25z" /></g><g transform="translate(0, 20) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M10 22.785q-1.125 0-1.773.602-.641.601-.641 1.656t.64 1.656q.649.602 1.774.602t1.773-.602q.649-.61.649-1.656 0-1.055-.649-1.656-.64-.602-1.773-.602zm-1.578-.672q-1.016-.25-1.586-.945-.563-.695-.563-1.695 0-1.399.993-2.211 1-.813 2.734-.813 1.742 0 2.734.813.993.812.993 2.21 0 1-.57 1.696-.563.695-1.571.945 1.14.266 1.773 1.04.641.773.641 1.89 0 1.695-1.04 2.602-1.03.906-2.96.906t-2.969-.906Q6 26.738 6 25.043q0-1.117.64-1.89.641-.774 1.782-1.04zm-.578-2.492q0 .906.562 1.414.57.508 1.594.508 1.016 0 1.586-.508.578-.508.578-1.414 0-.906-.578-1.414-.57-.508-1.586-.508-1.023 0-1.594.508-.562.508-.562 1.414z" /></g><g transform="translate(375, 20) scale(0.75, 0.75)" fill="#e5e5e5" stroke="#e5e5e5"><path d="M10 22.785q-1.125 0-1.773.602-.641.601-.641 1.656t.64 1.656q.649.602 1.774.602t1.773-.602q.649-.61.649-1.656 0-1.055-.649-1.656-.64-.602-1.773-.602zm-1.578-.672q-1.016-.25-1.586-.945-.563-.695-.563-1.695 0-1.399.993-2.211 1-.813 2.734-.813 1.742 0 2.734.813.993.812.993 2.21 0 1-.57 1.696-.563.695-1.571.945 1.14.266 1.773 1.04.641.773.641 1.89 0 1.695-1.04 2.602-1.03.906-2.96.906t-2.969-.906Q6 26.738 6 25.043q0-1.117.64-1.89.641-.774 1.782-1.04zm-.578-2.492q0 .906.562 1.414.57.508 1.594.508 1.016 0 1.586-.508.578-.508.578-1.414 0-.906-.578-1.414-.57-.508-1.586-.508-1.023 0-1.594.508-.562.508-.562 1.414z" /></g><rect x="15" y="330" width="45" height="45" class="square dark a1" stroke="none" fill="#d18b47" /><rect x="60" y="330" width="45" height="45" class="square light b1" stroke="none" fill="#ffce9e" /><rect x="105" y="330" width="45" height="45" class="square dark c1" stroke="none" fill="#d18b47" /><rect x="150" y="330" width="45" height="45" class="square light d1" stroke="none" fill="#ffce9e" /><rect x="195" y="330" width="45" height="45" class="square dark e1" stroke="none" fill="#d18b47" /><rect x="240" y="330" width="45" height="45" class="square light f1" stroke="none" fill="#ffce9e" /><rect x="285" y="330" width="45" height="45" class="square dark g1" stroke="none" fill="#d18b47" /><rect x="330" y="330" width="45" height="45" class="square light h1" stroke="none" fill="#ffce9e" /><rect x="15" y="285" width="45" height="45" class="square light a2" stroke="none" fill="#ffce9e" /><rect x="60" y="285" width="45" height="45" class="square dark b2" stroke="none" fill="#d18b47" /><rect x="105" y="285" width="45" height="45" class="square light c2" stroke="none" fill="#ffce9e" /><rect x="150" y="285" width="45" height="45" class="square dark d2" stroke="none" fill="#d18b47" /><rect x="195" y="285" width="45" height="45" class="square light e2" stroke="none" fill="#ffce9e" /><rect x="240" y="285" width="45" height="45" class="square dark f2" stroke="none" fill="#d18b47" /><rect x="285" y="285" width="45" height="45" class="square light g2" stroke="none" fill="#ffce9e" /><rect x="330" y="285" width="45" height="45" class="square dark h2" stroke="none" fill="#d18b47" /><rect x="15" y="240" width="45" height="45" class="square dark a3" stroke="none" fill="#d18b47" /><rect x="60" y="240" width="45" height="45" class="square light b3" stroke="none" fill="#ffce9e" /><rect x="105" y="240" width="45" height="45" class="square dark c3" stroke="none" fill="#d18b47" /><rect x="150" y="240" width="45" height="45" class="square light d3" stroke="none" fill="#ffce9e" /><rect x="195" y="240" width="45" height="45" class="square dark e3" stroke="none" fill="#d18b47" /><rect x="240" y="240" width="45" height="45" class="square light f3" stroke="none" fill="#ffce9e" /><rect x="285" y="240" width="45" height="45" class="square dark g3" stroke="none" fill="#d18b47" /><rect x="330" y="240" width="45" height="45" class="square light h3" stroke="none" fill="#ffce9e" /><rect x="15" y="195" width="45" height="45" class="square light a4" stroke="none" fill="#ffce9e" /><rect x="60" y="195" width="45" height="45" class="square dark b4" stroke="none" fill="#d18b47" /><rect x="105" y="195" width="45" height="45" class="square light c4" stroke="none" fill="#ffce9e" /><rect x="150" y="195" width="45" height="45" class="square dark d4" stroke="none" fill="#d18b47" /><rect x="195" y="195" width="45" height="45" class="square light e4" stroke="none" fill="#ffce9e" /><rect x="240" y="195" width="45" height="45" class="square dark f4" stroke="none" fill="#d18b47" /><rect x="285" y="195" width="45" height="45" class="square light g4" stroke="none" fill="#ffce9e" /><rect x="330" y="195" width="45" height="45" class="square dark h4" stroke="none" fill="#d18b47" /><rect x="15" y="150" width="45" height="45" class="square dark a5" stroke="none" fill="#d18b47" /><rect x="60" y="150" width="45" height="45" class="square light b5" stroke="none" fill="#ffce9e" /><rect x="105" y="150" width="45" height="45" class="square dark c5" stroke="none" fill="#d18b47" /><rect x="150" y="150" width="45" height="45" class="square light d5" stroke="none" fill="#ffce9e" /><rect x="195" y="150" width="45" height="45" class="square dark e5" stroke="none" fill="#d18b47" /><rect x="240" y="150" width="45" height="45" class="square light f5" stroke="none" fill="#ffce9e" /><rect x="285" y="150" width="45" height="45" class="square dark g5" stroke="none" fill="#d18b47" /><rect x="330" y="150" width="45" height="45" class="square light h5" stroke="none" fill="#ffce9e" /><rect x="15" y="105" width="45" height="45" class="square light a6" stroke="none" fill="#ffce9e" /><rect x="60" y="105" width="45" height="45" class="square dark b6" stroke="none" fill="#d18b47" /><rect x="105" y="105" width="45" height="45" class="square light c6" stroke="none" fill="#ffce9e" /><rect x="150" y="105" width="45" height="45" class="square dark d6" stroke="none" fill="#d18b47" /><rect x="195" y="105" width="45" height="45" class="square light e6" stroke="none" fill="#ffce9e" /><rect x="240" y="105" width="45" height="45" class="square dark f6" stroke="none" fill="#d18b47" /><rect x="285" y="105" width="45" height="45" class="square light g6" stroke="none" fill="#ffce9e" /><rect x="330" y="105" width="45" height="45" class="square dark h6" stroke="none" fill="#d18b47" /><rect x="15" y="60" width="45" height="45" class="square dark a7" stroke="none" fill="#d18b47" /><rect x="60" y="60" width="45" height="45" class="square light b7" stroke="none" fill="#ffce9e" /><rect x="105" y="60" width="45" height="45" class="square dark c7" stroke="none" fill="#d18b47" /><rect x="150" y="60" width="45" height="45" class="square light d7" stroke="none" fill="#ffce9e" /><rect x="195" y="60" width="45" height="45" class="square dark e7" stroke="none" fill="#d18b47" /><rect x="240" y="60" width="45" height="45" class="square light f7" stroke="none" fill="#ffce9e" /><rect x="285" y="60" width="45" height="45" class="square dark g7" stroke="none" fill="#d18b47" /><rect x="330" y="60" width="45" height="45" class="square light h7" stroke="none" fill="#ffce9e" /><rect x="15" y="15" width="45" height="45" class="square light a8" stroke="none" fill="#ffce9e" /><rect x="60" y="15" width="45" height="45" class="square dark b8" stroke="none" fill="#d18b47" /><rect x="105" y="15" width="45" height="45" class="square light c8" stroke="none" fill="#ffce9e" /><rect x="150" y="15" width="45" height="45" class="square dark d8" stroke="none" fill="#d18b47" /><rect x="195" y="15" width="45" height="45" class="square light e8" stroke="none" fill="#ffce9e" /><rect x="240" y="15" width="45" height="45" class="square dark f8" stroke="none" fill="#d18b47" /><rect x="285" y="15" width="45" height="45" class="square light g8" stroke="none" fill="#ffce9e" /><rect x="330" y="15" width="45" height="45" class="square dark h8" stroke="none" fill="#d18b47" /><use href="#white-rook" xlink:href="#white-rook" transform="translate(15, 330)" /><use href="#white-knight" xlink:href="#white-knight" transform="translate(60, 330)" /><use href="#white-bishop" xlink:href="#white-bishop" transform="translate(105, 330)" /><use href="#white-queen" xlink:href="#white-queen" transform="translate(150, 330)" /><use href="#white-king" xlink:href="#white-king" transform="translate(195, 330)" /><use href="#white-bishop" xlink:href="#white-bishop" transform="translate(240, 330)" /><use href="#white-knight" xlink:href="#white-knight" transform="translate(285, 330)" /><use href="#white-rook" xlink:href="#white-rook" transform="translate(330, 330)" /><use href="#white-pawn" xlink:href="#white-pawn" transform="translate(15, 285)" /><use href="#white-pawn" xlink:href="#white-pawn" transform="translate(60, 285)" /><use href="#white-pawn" xlink:href="#white-pawn" transform="translate(105, 285)" /><use href="#white-pawn" xlink:href="#white-pawn" transform="translate(150, 285)" /><use href="#white-pawn" xlink:href="#white-pawn" transform="translate(195, 285)" /><use href="#white-pawn" xlink:href="#white-pawn" transform="translate(240, 285)" /><use href="#white-pawn" xlink:href="#white-pawn" transform="translate(285, 285)" /><use href="#white-pawn" xlink:href="#white-pawn" transform="translate(330, 285)" /><use href="#black-pawn" xlink:href="#black-pawn" transform="translate(15, 60)" /><use href="#black-pawn" xlink:href="#black-pawn" transform="translate(60, 60)" /><use href="#black-pawn" xlink:href="#black-pawn" transform="translate(105, 60)" /><use href="#black-pawn" xlink:href="#black-pawn" transform="translate(150, 60)" /><use href="#black-pawn" xlink:href="#black-pawn" transform="translate(195, 60)" /><use href="#black-pawn" xlink:href="#black-pawn" transform="translate(240, 60)" /><use href="#black-pawn" xlink:href="#black-pawn" transform="translate(285, 60)" /><use href="#black-pawn" xlink:href="#black-pawn" transform="translate(330, 60)" /><use href="#black-rook" xlink:href="#black-rook" transform="translate(15, 15)" /><use href="#black-knight" xlink:href="#black-knight" transform="translate(60, 15)" /><use href="#black-bishop" xlink:href="#black-bishop" transform="translate(105, 15)" /><use href="#black-queen" xlink:href="#black-queen" transform="translate(150, 15)" /><use href="#black-king" xlink:href="#black-king" transform="translate(195, 15)" /><use href="#black-bishop" xlink:href="#black-bishop" transform="translate(240, 15)" /><use href="#black-knight" xlink:href="#black-knight" transform="translate(285, 15)" /><use href="#black-rook" xlink:href="#black-rook" transform="translate(330, 15)" /></svg>',
        "move_time" : move_time,
        "start_timer" : time.time(),
        "white" : 0,
        "black" : 0,
        "draw" : 0,
        "white_tweets" : [],
        "black_tweets" : [],
        "history" : [],
        "history_white" : [],
        "history_black" : [],
        "last_win": "",
        "game_ending": ""
    }

    return game

# reset game in corso
def reset(game):
    game["playing"] = False
    game["side"] = True
    game["board"] = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    game["boardsvg"] = ""
    game["move_time"] = 1
    game["start_timer"] = ""
    game["white_tweets"] = []
    game["black_tweets"] = []
    game["history"] = []
    game["history_white"] = []
    game["history_black"] = []
    game["draw"] += 1
    game["last_win"] = "Sport"

    return game

#End the chess game from the game list
def end_game(game, board):
    game["playing"] = False
    game["side"] = True
    game["board"] = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    game["boardsvg"] = ""
    game["move_time"] = 1
    game["start_timer"] = ""
    game["white_tweets"] = []
    game["black_tweets"] = []
    game["history"] = []
    game["history_white"] = []
    game["history_black"] = []
    ending = board.outcome()
    side = ending.winner
    game["game_ending"] = ending.termination.name
    if side == True:
        game["white"] += 1
        game["last_win"] = "Bianco"
        
    elif side == False:
        game["black"] += 1
        game["last_win"] = "Nero"
    else :
        game["draw"] += 1
        game["last_win"] = "Sport"

    return game


#Get the last tweet of the specified user
def get_user_last_tweet(user):
    filtri = {}
    filtri["username"] = user

    tweet_list, _ = TAPI.get_tweets(filtri, {})
    tweet_list = json.loads(tweet_list)

    if tweet_list.get("data", None) != None and len(tweet_list["data"]) > 0:#se abbiamo ottenuto dei risultati
        return tweet_list
    return None #stringa vuota per non matchare sull'hashtag di inizio partita
    


#Get a random move
def get_random_move(board):
    legal_moves_list = list(board.legal_moves)
    move = legal_moves_list[random.randint(0, board.legal_moves.count() - 1)]

    return move.uci()


#Get the wanted move from the white player tweet
def get_user_move(board, user):
    tweet_list = get_user_last_tweet(user)
    if tweet_list != {}:
        tweet = tweet_list["data"][0]["text"].lower()
        tweet = tweet.split()
    move = ""
    #Find a valid move in the last user tweet
    for word in tweet:
        for valid_move in list(board.legal_moves):
            if valid_move.uci() == word:
                move = word

    if move == "":
        return get_random_move(board), tweet_list

    move = board.parse_san(move).uci()
    return move, tweet_list


#Get the wanted move from the black players tweet
def get_mass_move(board, user):
    filtri = {}
    filtri["hashtag"] = user

    opzioni = {}
    opzioni["max_tweets"] = 50
    data_oggi = str(date.today())
    now = datetime.now()
    now = now - timedelta(hours=1)
    query_time = now.strftime("%H:%M:%S")
    opzioni["data_inizio"] = data_oggi+"T"+query_time+"+01:00"

    tweet_list, occurrences_list = TAPI.get_tweets(filtri, opzioni)
    tweet_list = json.loads(tweet_list)
    occurrences_list = json.loads(occurrences_list)


    move = ""
    move_occurrences = 0

    if occurrences_list != []:
        for word in occurrences_list:
            #print(word)
            for valid_move in list(board.legal_moves):
                if valid_move.uci() == word["text"]:
                    if word["size"] > move_occurrences:
                        move_occurrences = word["size"]
                        move = word["text"]

    if move == "":
        return get_random_move(board), tweet_list

    return move, tweet_list


#Make the given move
def make_move(game):
    board = chess.Board(game["board"])
    reset = ""

    if board.turn:
        move, tweet_list = get_user_move(board, game["tweetaccount"])
        if tweet_list != {}:
            reset = tweet_list["data"][0]["text"].lower()
            first_tweet = {}
            first_tweet["data"] = [tweet_list["data"][0]]
            game["white_tweets"].append(first_tweet)
        game["history_white"].append(move)
    else :
        move, tweet_list = get_mass_move(board, game["tweetaccount"])
        game["black_tweets"].append(tweet_list)
        game["history_black"].append(move)


    board.push_san(move)
    game["history"].append(move)

    game["side"] = board.turn
    
    game["board"] = board.fen()

    game["boardsvg"] = chess.svg.board(board)

    game["start_timer"] = time.time()

    #Check if the board is valid and the game can continue
    if board.is_game_over():
        #or can_claim_draw() may be slow
        return end_game(game, board), False

    for word in reset:
        if word == "reset":
            return reset(game), False

    return game, True

#Update the game with the last move or add a new game
#to the JSON list of games 
def update_games_list(opzioni, progress):
    user = opzioni["username"].lower()
    move_time = int(opzioni["move_time"])

    #Read JSON file
    with open(games_file, 'r+') as file:
        games_list = json.load(file)

    #Update the game
    for game in games_list["games"]:
        if game["tweetaccount"] == user:
            if game["playing"] == True and progress == False:
                #If game already exist and is running return it
                return True, game
            break

    
    #Check if user tweetted #startchesstweetutils
    if progress == False:
        tweet_list = get_user_last_tweet(user)
        if tweet_list != None:
            tweet_text = tweet_list["data"][0]["text"]
            first_tweet = {}
            first_tweet["data"] = [tweet_list["data"][0]]
            if "startchesstweetutils" in tweet_text:
                if game["tweetaccount"] == user:
                    game["playing"] = True
                    game["start_timer"] = time.time()
                    game["white_tweets"].append(first_tweet)
                else :
                    #Create a new game and add it to the games list
                    game = start_game(user, move_time)
                    game["start_timer"] = time.time()
                    game["white_tweets"].append(first_tweet)
                    games_list["games"].append(game)                
        else :
            #User didn't tweet so the game isn't started
            return False, {}


    board_valid = True
    if progress == True:
        #Make a move, control and update if a game ends
        game, board_valid = make_move(game)

    #Save JSON file
    with open(games_file, 'w') as file:
        json.dump(games_list, file, indent = 4)


    if board_valid:
        return True, game
    return False, game
