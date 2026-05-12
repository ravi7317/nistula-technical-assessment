-- Nistula Unified Messaging Platform Schema
-- PostgreSQL

-- 1. Guest Profiles: Stores unique guest information across all channels.
-- A guest is identified by a unique combination of name and contact info (if available), 
-- but for this schema, we use a global guest_id.
CREATE TABLE guests (
    guest_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Properties: Basic property information.
CREATE TABLE properties (
    property_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    details JSONB
);

-- 3. Reservations: Links guests to properties and specific booking references.
CREATE TABLE reservations (
    reservation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_ref VARCHAR(50) UNIQUE NOT NULL,
    guest_id UUID REFERENCES guests(guest_id),
    property_id VARCHAR(50) REFERENCES properties(property_id),
    check_in DATE,
    check_out DATE,
    status VARCHAR(50), -- confirmed, cancelled, stayed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Conversations: Groups messages between a guest and the platform for a specific reservation/context.
CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_id UUID REFERENCES guests(guest_id),
    reservation_id UUID REFERENCES reservations(reservation_id),
    last_message_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active' -- active, closed, archived
);

-- 5. Messages: Stores all inbound and outbound messages across all channels.
CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(conversation_id),
    sender_type VARCHAR(20) NOT NULL, -- 'guest', 'ai', 'agent'
    source VARCHAR(50) NOT NULL, -- whatsapp, booking_com, airbnb, instagram, direct
    message_text TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- AI Metadata (for inbound messages or AI-generated outbound)
    query_type VARCHAR(50), -- pre_sales_availability, complaint, etc.
    ai_confidence_score DECIMAL(3, 2),
    
-- 5. Delivery Status Mapping:
-- - 'drafted': AI generated message awaiting review.
-- - 'sent': Auto-sent by AI (if confidence > 0.85).
-- - 'edited_and_sent': Message was AI-drafted but edited by an agent before sending.
-- - 'failed': Message could not be delivered.
    delivery_status VARCHAR(50), 
    
    -- Link to original message if this is a reply
    reply_to_id UUID REFERENCES messages(message_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Design Decisions & Comments:
-- 1. Guest Normalization: Used a central 'guests' table to track the same person across different 
--    booking channels (Airbnb, WhatsApp, etc.). In a real system, we would need a sophisticated 
--    identity matching logic (e.g., matching by phone or email).
-- 2. Conversation Grouping: Added 'conversations' to provide context. Messaging is rarely a single 
--    event; it's a flow. Linking to 'reservations' allows the AI to pull context like check-in dates.
-- 3. Unified Message Table: Decided to keep all messages in one table with a 'sender_type' and 
--    'source' to simplify reporting and cross-channel history viewing.
-- 4. AI Metadata: Included 'query_type' and 'ai_confidence_score' directly in the messages table 
--    to ensure every inbound message is classified and tracked.
-- 5. Delivery Status: Added 'delivery_status' to distinguish between 'ai_drafted', 'agent_edited', 
--    and 'auto_sent' (mapped to 'sent').

-- Hardest Design Decision:
-- The hardest decision was whether to make 'conversations' strictly linked to 'reservations'. 
-- Guests often message before they have a booking reference (pre-sales). I chose to make 
-- reservation_id NULLABLE in the conversations table to support the full guest lifecycle 
-- from enquiry to post-stay feedback. This adds complexity in query logic but is necessary 
-- for a realistic hospitality CRM.
