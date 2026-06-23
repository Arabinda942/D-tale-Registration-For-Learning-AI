# -*- coding: utf-8 -*-
"""Generates the welcome / login-credentials PDF handed to a student right
after registration."""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas


GOLD = colors.HexColor("#E6A300")
NAVY = colors.HexColor("#10162C")
SLATE = colors.HexColor("#5B6479")
LINE = colors.HexColor("#E7E9F2")


def build_credentials_pdf(name, username, password, email, phone):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    # Header band
    c.setFillColor(NAVY)
    c.rect(0, height - 40 * mm, width, 40 * mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(20 * mm, height - 20 * mm, "D'TALE LEARNING CENTER")
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 11)
    c.drawString(20 * mm, height - 28 * mm, "Learn Today, Lead Tomorrow")
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(20 * mm, height - 34 * mm, "120-Day AI Learning Journey \u2014 Student Portal")

    y = height - 55 * mm

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, y, f"Welcome, {name}!")
    y -= 8 * mm
    c.setFont("Helvetica", 10.5)
    c.setFillColor(SLATE)
    c.drawString(20 * mm, y, "Your registration is complete. Keep this page \u2014 you'll need it to log in.")
    y -= 14 * mm

    # Credentials box
    box_top = y
    box_height = 38 * mm
    c.setStrokeColor(LINE)
    c.setLineWidth(1)
    c.setFillColor(colors.HexColor("#FAFAFC"))
    c.roundRect(20 * mm, box_top - box_height, width - 40 * mm, box_height, 4 * mm, fill=1, stroke=1)

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(28 * mm, box_top - 8 * mm, "YOUR LOGIN CREDENTIALS")

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(28 * mm, box_top - 18 * mm, "Student ID (username):")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(95 * mm, box_top - 18.7 * mm, username)

    c.setFont("Helvetica-Bold", 11)
    c.drawString(28 * mm, box_top - 28 * mm, "Password:")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(95 * mm, box_top - 28.7 * mm, password)

    y = box_top - box_height - 12 * mm

    c.setFillColor(SLATE)
    c.setFont("Helvetica", 9.5)
    c.drawString(20 * mm, y, f"Registered with: {email}   \u00b7   {phone}")
    y -= 10 * mm

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(20 * mm, y, "How the course works:")
    y -= 7 * mm
    c.setFont("Helvetica", 9.5)
    c.setFillColor(SLATE)
    lines = [
        "\u2022  Log in at the Student Login page using the ID and password above.",
        "\u2022  Chapter 1 is unlocked first. Every chapter has 50 short assignments.",
        "\u2022  Complete all 50 assignments in a chapter to unlock the next one.",
        "\u2022  After all 42 chapters, 10 capstone projects unlock in the same way.",
        "\u2022  Keep this PDF safe \u2014 your password is not shown again after this page.",
    ]
    for line in lines:
        c.drawString(20 * mm, y, line)
        y -= 6 * mm

    y -= 6 * mm
    c.setStrokeColor(LINE)
    c.line(20 * mm, y, width - 20 * mm, y)
    y -= 8 * mm
    c.setFont("Helvetica-Oblique", 8.5)
    c.setFillColor(SLATE)
    c.drawString(20 * mm, y, "D'TALE Learning Center \u00b7 Your Success, Our Mission")

    c.showPage()
    c.save()
    buf.seek(0)
    return buf
