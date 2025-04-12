from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.metrics import dp
from kivy.animation import Animation
import requests


def fetch_stats():
    xla = requests.get("https://fastpool.xyz/api-xla/stats_address?address=SvmBebtVdKnVHdY5Hd9GRDLcgtU41ah52eoYkkQQ5E94gyHNbvhrgZpCAdXFi7N3FjUB6d29xSFxcLHbjJx5mFoa2Ur8KLSuo").json()
    salv = requests.get("https://fastpool.xyz/api-sal/stats_address?address=SaLvdYnwkBS1st1FLwrJ9fawNdZP7aVNLfUj2QhieR5VhpG3jRcF2dNcZuQyCzFQCeWcv2rMN3FY7Q38dwQZpY9E7pr9B8DDWvP").json()
    return xla, salv


def format_hashrate(hr):
    if hr >= 1e12:
        return f"{hr / 1e12:.2f} TH/s"
    elif hr >= 1e9:
        return f"{hr / 1e9:.2f} GH/s"
    elif hr >= 1e6:
        return f"{hr / 1e6:.2f} MH/s"
    elif hr >= 1e3:
        return f"{hr / 1e3:.2f} kH/s"
    else:
        return f"{hr:.2f} H/s"


class StatsApp(App):
    def build(self):
        self.title = "hashmon"
        self.root_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        self.progress = ProgressBar(max=30, value=0, size_hint_y=None, height=dp(10))
        self.root_layout.add_widget(self.progress)

        self.refresh_button = Button(text="Refresh", size_hint_y=None, height=dp(50), font_size='18sp')
        self.refresh_button.bind(on_press=lambda _: self.update_stats(force=True))
        self.root_layout.add_widget(self.refresh_button)

        self.scroll = ScrollView()
        self.stats_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10), padding=(0, dp(10)))
        self.stats_layout.bind(minimum_height=self.stats_layout.setter('height'))
        self.scroll.add_widget(self.stats_layout)
        self.root_layout.add_widget(self.scroll)

        self.timer = 0
        Clock.schedule_interval(self.update_progress, 1)
        self.update_stats(force=True)
        return self.root_layout

    def update_progress(self, dt):
        self.timer += 1
        self.progress.value = self.timer
        if self.timer >= 30:
            self.update_stats(force=True)

    def update_stats(self, force=False):
        self.timer = 0
        self.progress.value = 0

        def replace_stats(*_):
            self.stats_layout.clear_widgets()
            xla, salv = fetch_stats()
            for name, data in [("XLA", xla), ("SALV", salv)]:
                self.stats_layout.add_widget(Label(text=name, bold=True, font_size='26sp', size_hint_y=None, height=dp(36)))

                workers = data.get("workers", [])
                workers = [w for w in workers if w["hashrate"] > 0]
                workers.sort(key=lambda x: x["name"].lower())
                max_hr = max([w["hashrate"] for w in workers], default=0)

                for w in workers:
                    row = BoxLayout(size_hint_y=None, height=dp(36))
                    name_label = Label(text=w["name"], halign="left", bold=True, size_hint_x=0.5)
                    hr_label = Label(text=format_hashrate(w["hashrate"]), halign="right", size_hint_x=0.5)
                    name_label.text_size = (None, None)
                    hr_label.text_size = (None, None)
                    if w["hashrate"] == max_hr:
                        name_label.color = (0, 1, 0, 1)
                        hr_label.color = (0, 1, 0, 1)
                    row.add_widget(name_label)
                    row.add_widget(hr_label)
                    self.stats_layout.add_widget(row)

        anim = Animation(opacity=0, duration=0.3) + Animation(opacity=1, duration=0.3)
        anim.bind(on_complete=replace_stats)
        anim.start(self.stats_layout)


if __name__ == '__main__':
    StatsApp().run()
