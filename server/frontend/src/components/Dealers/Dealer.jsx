import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./Dealer.css";
import "../assets/style.css";

import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";

import Header from "../Header/Header";

const Dealer = () => {
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReviewButton, setPostReviewButton] = useState(null);

  const { id } = useParams();

  // Build URLs cleanly
  const root = window.location.origin + "/";
  const dealer_url = `${root}djangoapp/dealer/${id}`;
  const reviews_url = `${root}djangoapp/reviews/dealer/${id}`;
  const post_review_url = `${root}postreview/${id}`;

  // Fetch dealer details
  const get_dealer = async () => {
    const res = await fetch(dealer_url);
    const data = await res.json();

    if (data.status === 200) {
      setDealer(data.dealer); // dealer is an object
    }
  };

  // Fetch reviews
  const get_reviews = async () => {
    const res = await fetch(reviews_url);
    const data = await res.json();

    if (data.status === 200) {
      if (data.reviews.length > 0) {
        setReviews(data.reviews);
      } else {
        setUnreviewed(true);
      }
    }
  };

  // Choose sentiment icon
  const senti_icon = (sentiment) => {
    if (sentiment === "positive") return positive_icon;
    if (sentiment === "negative") return negative_icon;
    return neutral_icon;
  };

  useEffect(() => {
    get_dealer();
    get_reviews();

    if (sessionStorage.getItem("username")) {
      setPostReviewButton(
        <a href={post_review_url} className="review-button">
          <img src={review_icon} alt="Post Review" />
        </a>
      );
    }
  }, []);

  // Prevent white screen while loading
  if (!dealer) {
    return (
      <div className="dealer-container">
        <Header />
        <h2 className="loading-text">Loading dealer...</h2>
      </div>
    );
  }

  return (
    <div className="dealer-container">
      <Header />

      <div className="dealer-header">
        <h1>
          {dealer.full_name}
          {postReviewButton}
        </h1>

        <h4>
          {dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}
        </h4>
      </div>

      <div className="reviews_panel">
        {reviews.length === 0 && !unreviewed ? (
          <div className="loading-text">Loading Reviews...</div>
        ) : unreviewed ? (
          <div className="no-reviews">No reviews yet!</div>
        ) : (
          reviews.map((review) => (
            <div className="review_panel" key={review.id}>
              <img
                src={senti_icon(review.sentiment)}
                className="emotion_icon"
                alt="Sentiment"
              />
              <div>
                <div className="review">{review.review}</div>
                <div className="reviewer">
                  {review.name} {review.car_make} {review.car_model}{" "}
                  {review.car_year}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dealer;