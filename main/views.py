from django.shortcuts import render, get_object_or_404
from accounts.models import Movie, Cinema, Shows, Bookings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Home Page: Display all movies
def index(request):
    movies = Movie.objects.all()
    return render(request, "index.html", {'mov': movies})

# Movie Details: Show available cinemas and showtimes
def movies(request, id):
    movie = get_object_or_404(Movie, movie=id)  # ✅ Fix: Use 'movie' instead of 'id'
    cinemas = Cinema.objects.filter(cinema_show__movie=movie).distinct()
    shows = Shows.objects.filter(movie=movie)

    return render(request, "movies.html", {
        'movies': movie,
        'show': shows,
        'cin': cinemas,
    })

# Seat Selection: Display available seats
def seat(request, id):
    show = get_object_or_404(Shows, shows=id)  # ✅ Fix: Use 'shows' instead of 'id'
    booked_seats = Bookings.objects.filter(shows=show).values_list('useat', flat=True)

    return render(request, "seat.html", {'show': show, 'booked_seats': booked_seats})

# Booking Confirmation: Process booking and send email
@login_required
def booked(request):
    if request.method == 'POST':
        user = request.user
        seat_list = request.POST.getlist('check')
        show_id = request.POST.get('show')

        if not seat_list:
            return JsonResponse({"error": "No seats selected!"}, status=400)

        show = get_object_or_404(Shows, shows=show_id)  # ✅ Fix: Use 'shows' instead of 'id'
        seat_numbers = ', '.join(seat_list)

        # Save booking
        booking = Bookings.objects.create(user=user, shows=show, useat=seat_numbers)

        # Send confirmation email
        subject = "🎟️ Booking Confirmation"
        message = f"""
        Dear {user.first_name},

        Your booking has been confirmed!

        🎬 Movie: {show.movie.movie_name}
        📍 Cinema: {show.cinema.cinema_name}
        📅 Date: {show.date}
        ⏰ Time: {show.time}
        🎟️ Seats: {seat_numbers}
        💰 Price: ₹{show.price}

        Thank you for booking with us!
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            print(f"❌ Error sending email: {e}")

        return render(request, "booked.html", {'book': booking})

    return JsonResponse({"error": "Invalid request!"}, status=400)

# Ticket Page: Display ticket details
@login_required
def ticket(request, id):
    ticket = get_object_or_404(Bookings, id=id)
    return render(request, "ticket.html", {'ticket': ticket})

# Chatbot API (Dummy)
def chatbot(request):
    return JsonResponse({"message": "Hello, I am your chatbot!"})
