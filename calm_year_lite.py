#!/usr/bin/env python3
"""Calm Year 2027 Lite - builds a small printable planner PDF.

Pages: 2027 at a glance, 12 monthly calendars, 1 blank weekly page, 1 invoice log page.
Needs: Python 3.8+ and reportlab (pip install reportlab). No network access.
Writes exactly one PDF into the output folder; never overwrites without --force.
"""
import argparse
import calendar
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

YEAR = 2027
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
INK, MUTE, LINE = HexColor("#33424B"), HexColor("#7B8A90"), HexColor("#CBD6D1")
SOFT, ACC = HexColor("#EEF3F0"), HexColor("#4C7A66")


class Doc:
    def __init__(self, path, size):
        self.c = canvas.Canvas(str(path), pagesize=size)
        self.c.setTitle("Calm Year 2027 Lite")
        self.c.setAuthor("Blixwerk")
        self.W, self.H = size
        self.x0, self.x1 = 16 * mm, self.W - 16 * mm
        self.y0, self.y1 = 16 * mm, self.H - 16 * mm
        self.n = 0

    def page(self, title, right=None):
        if self.n:
            self.c.showPage()
        self.n += 1
        c = self.c
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(self.x0, self.y1 - 18, title)
        if right:
            c.setFillColor(ACC)
            c.setFont("Helvetica", 12)
            c.drawRightString(self.x1, self.y1 - 18, right)
        c.setStrokeColor(ACC)
        c.setLineWidth(1.6)
        c.line(self.x0, self.y1 - 28, self.x0 + 28, self.y1 - 28)
        c.setFillColor(MUTE)
        c.setFont("Helvetica", 7)
        c.drawString(self.x0, 8 * mm, "Calm Year 2027 Lite - Blixwerk - MIT licence")
        c.drawRightString(self.x1, 8 * mm, str(self.n))
        return self.y1 - 42

    def line(self, x0, y0, x1, y1, w=0.6):
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(w)
        self.c.line(x0, y0, x1, y1)

    def text(self, x, y, s, size=9, bold=False, col=INK, al="l"):
        c = self.c
        c.setFillColor(col)
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        {"l": c.drawString, "c": c.drawCentredString, "r": c.drawRightString}[al](x, y, s)

    def ruled(self, x0, x1, top, bot, label, gap=19, boxes=False):
        self.text(x0, top - 8, label.upper(), 6.8, True, ACC)
        y = top - 12 - gap
        while y >= bot - 0.5:
            self.line(x0, y, x1, y)
            if boxes:
                self.c.setStrokeColor(MUTE)
                self.c.rect(x0, y + 3, 7, 7, stroke=1, fill=0)
            y -= gap


def page_year(d):
    y = d.page("2027 at a glance")
    gap, ncol, nrow = 10, 3, 4
    w = (d.x1 - d.x0 - gap * (ncol - 1)) / ncol
    h = (y - d.y0 - gap * (nrow - 1)) / nrow
    cal = calendar.Calendar(0)
    for m in range(1, 13):
        r, ci = divmod(m - 1, ncol)
        x, top = d.x0 + ci * (w + gap), y - r * (h + gap)
        d.text(x, top - 9, MONTHS[m - 1], 9.5, True)
        d.line(x, top - 14, x + w, top - 14)
        dw = w / 7
        for i, ch in enumerate("MTWTFSS"):
            d.text(x + dw * i + dw / 2, top - 23, ch, 6, True, ACC, "c")
        rh = (h - 28) / 6
        for ri, wk in enumerate(cal.monthdayscalendar(YEAR, m)):
            for di, day in enumerate(wk):
                if day:
                    d.text(x + dw * di + dw / 2, top - 28 - ri * rh - rh / 2 - 2,
                           str(day), 7, False, MUTE if di >= 5 else INK, "c")


def page_month(d, m):
    y = d.page(MONTHS[m - 1], str(YEAR))
    cal = calendar.Calendar(0).monthdayscalendar(YEAR, m)
    nr = len(cal)
    cw = (d.x1 - d.x0) / 7
    cal_bot = d.y0 + 0.23 * (y - d.y0) + 12
    gt = y - 15
    rh = (gt - cal_bot) / nr
    for i in range(7):
        d.text(d.x0 + cw * i + cw / 2, y - 10, DAYS[i], 7, True, ACC, "c")
    d.c.setFillColor(SOFT)
    for r in range(nr):
        d.c.rect(d.x0 + 5 * cw, gt - (r + 1) * rh, 2 * cw, rh, stroke=0, fill=1)
    for r in range(nr + 1):
        d.line(d.x0, gt - r * rh, d.x1, gt - r * rh)
    for i in range(8):
        d.line(d.x0 + i * cw, gt, d.x0 + i * cw, gt - nr * rh)
    for r, wk in enumerate(cal):
        for ci, day in enumerate(wk):
            if day:
                d.text(d.x0 + ci * cw + 4, gt - r * rh - 10, str(day), 8, ci < 5)
    by = cal_bot - 12
    mid = (d.x0 + d.x1) / 2
    d.ruled(d.x0, mid - 7, by, d.y0, "Dates that matter", 17)
    d.ruled(mid + 7, d.x1, by, d.y0, "This month's focus", 17)


def page_week(d):
    y = d.page("Week", "__ / __ / 2027  -  __ / __ / 2027")
    d.ruled(d.x0, d.x1, y, y - 90, "Top 3 priorities", 24, boxes=True)
    top = y - 100
    d.text(d.x0, top - 8, "THE WEEK", 6.8, True, ACC)
    d.text(d.x1, top - 8, "Billable h", 6.5, False, MUTE, "r")
    t0 = top - 12
    bottom = d.y0 + 70
    rh = (t0 - bottom) / 7
    for r in range(7):
        if r >= 5:
            d.c.setFillColor(SOFT)
            d.c.rect(d.x0, t0 - (r + 1) * rh, d.x1 - d.x0, rh, stroke=0, fill=1)
    for r in range(8):
        d.line(d.x0, t0 - r * rh, d.x1, t0 - r * rh)
    for r in range(7):
        d.text(d.x0 + 3, t0 - r * rh - 11, DAYS[r], 8, True)
        d.c.setStrokeColor(LINE)
        d.c.roundRect(d.x1 - 30, t0 - (r + 1) * rh + 3, 30, rh - 6, 3, stroke=1, fill=0)
    d.ruled(d.x0, d.x1, bottom - 8, d.y0, "One calm win", 17)


def page_invoices(d):
    y = d.page("Invoice log", "Look at the Due column first")
    cols = [("No.", .12), ("Client", .28), ("Sent", .15), ("Due", .15), ("Amount", .16), ("Paid on", .14)]
    w, rows, hh = d.x1 - d.x0, 22, 18
    bottom = d.y0 + 10
    rh = (y - bottom - hh) / rows
    d.c.setFillColor(SOFT)
    d.c.rect(d.x0, y - hh, w, hh, stroke=0, fill=1)
    xs = [d.x0]
    for _, fr in cols:
        xs.append(xs[-1] + w * fr)
    xs[-1] = d.x1
    for i, (lab, _) in enumerate(cols):
        d.text(xs[i] + 4, y - hh + 6, lab.upper(), 6.8, True, ACC)
    for r in range(rows + 1):
        d.line(d.x0, y - hh - r * rh, d.x1, y - hh - r * rh)
    for xv in xs:
        d.line(xv, y, xv, y - hh - rows * rh)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the Calm Year 2027 Lite planner PDF.")
    ap.add_argument("--out", default="out", help="output folder (created if missing; default: ./out)")
    ap.add_argument("--paper", choices=["a4", "letter"], default="a4")
    ap.add_argument("--force", action="store_true", help="overwrite the PDF if it already exists")
    a = ap.parse_args(argv)
    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / ("Calm-Year-2027-Lite_%s.pdf" % a.paper.upper())
    if path.exists() and not a.force:
        print("Exists, not overwriting (use --force): %s" % path)
        return 1
    d = Doc(path, A4 if a.paper == "a4" else letter)
    page_year(d)
    for m in range(1, 13):
        page_month(d, m)
    page_week(d)
    page_invoices(d)
    d.c.save()
    print("Wrote %s (%d pages). Print at 100%% / Actual size." % (path, d.n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
