#!/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from time import time

from comparator import orb, common, comparator

class MainWindow(Gtk.Window):
    def __init__(self, target, neighbors=[]):
        Gtk.Window.__init__(self, title="Compare images")
        Gtk.Window.set_default_size(self, 1000, 800)

        self.main_box = Gtk.Box(spacing=6)
        self.add(self.main_box)

        self.main_box.pack_start(self.target_box(target), True,  True, 0)

        self.main_box.pack_start(self.previews(neighbors), True, True, 0)

    def previews(self, neighbors):
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(30)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)

        scrolled.add(flowbox)

        for image in neighbors:
            img = self.image_preview(*image)
            flowbox.add(img)

        return scrolled

    def image_preview(self, image_name, image_score):
        box = Gtk.Box(orientation="vertical")
        image_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_name, width=200, height=120,
                                                preserve_aspect_ratio=True)
        box.pack_start(Gtk.Image.new_from_pixbuf(image_pixbuf), True, True, 0)
        box.pack_start(Gtk.Label(image_name), True, True, 0)
        box.pack_start(Gtk.Label(image_score), True, True, 0)

        return box


    def target_box(self, target):
        box = Gtk.Box(orientation="vertical")
        self.target_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(target, width=600, height=400,
                                                preserve_aspect_ratio=True)
        self.target_img = Gtk.Image.new_from_pixbuf(self.target_pixbuf)
        box.pack_start(self.target_img, True, True, 0)
        box.pack_start(Gtk.Label(target), True, True, 0)

        return box


if __name__ == "__main__":
    t = time()
    target, candidates = common.parse_args()

    engine = orb

    features = engine.compute_features([target] + candidates)
    print("Features: {}s".format(time() - t))
    t = time()

    results = engine.find_nn(target, candidates, features)
    print("NN: {}s".format(time() - t))

    win = MainWindow(target, results)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()